package main

import (
	"bytes"
	"crypto/tls"
	"flag"
	"io"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
	"math/rand"

	quic "github.com/lucas-clemente/quic-go"

	"github.com/lucas-clemente/quic-go/h2quic"
	"github.com/lucas-clemente/quic-go/internal/utils"
)

func main() {
	verbose := flag.Bool("v", false, "verbose")
	multipath := flag.Bool("m", false, "multipath")
	output := flag.String("o", "", "logging output")
	cache := flag.Bool("c", false, "cache handshake information")
	flag.Parse()
	urls := flag.Args()

	if *verbose {
		utils.SetLogLevel(utils.LogLevelDebug)
	} else {
		utils.SetLogLevel(utils.LogLevelInfo)
	}

	if *output != "" {
		logfile, err := os.Create(*output)
		if err != nil {
			panic(err)
		}
		defer logfile.Close()
		log.SetOutput(logfile)
	}

	quicConfig := &quic.Config{
		CreatePaths:    *multipath,
		CacheHandshake: *cache,
	}

	hclient := &http.Client{
		Transport: &h2quic.RoundTripper{QuicConfig: quicConfig, TLSClientConfig: &tls.Config{InsecureSkipVerify: true}},
	}

	jsonStr := make([]byte, 3000000)
    	rand.Read(jsonStr)
	//jsonStr := []byte("Hi there, I love!")
	
	var wg sync.WaitGroup
	wg.Add(len(urls))
	for _, addr := range urls {
		utils.Infof("POST %s", addr)
		go func(addr string) {
			start := time.Now()
			rsp, err := hclient.Post(addr, "application/json", bytes.NewBuffer(jsonStr))
			if err != nil {
				panic(err)
			}

			utils.Infof("Got response for %s: %#v", addr, rsp)
			body := &bytes.Buffer{}
			_, err = io.Copy(body, rsp.Body)
			if err != nil {
				//panic(err)
				utils.Infof("%f", float64(30000))
				wg.Done()
			}else {
				elapsed := time.Since(start)
				utils.Infof("%f", float64(elapsed.Nanoseconds())/1000000)
			        utils.Infof("%s", body.Bytes())
				wg.Done()
			}
		}(addr)
	}
	wg.Wait()
}
