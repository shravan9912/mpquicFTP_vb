package main
 
import (
	"fmt"
        "time"
	"os"
)

const DetectAgentPath = "/home/mosaic/edge-computing-mpquic/output/"

type detectionAgent struct{
	detectionbase	[]float64
}

func (det * detectionAgent) Setup(){
	det.detectionbase = make([]float64,0)
}

func (det * detectionAgent) Clear(){
	det.detectionbase = nil
}

func (det * detectionAgent) AddStep(step float64){
        det.detectionbase = append(det.detectionbase, step)
}

func (det * detectionAgent) CloseExperience(num int, path string){

		fileName := fmt.Sprintf(path + "detectionAgent_%d.csv", num)

		file, err := os.Create(fileName)
		if err != nil{
			panic(err)
		}
		defer file.Close()
                fmt.Fprintf(file, "PathInfo\n")
		for _, element := range det.detectionbase{
                        fmt.Fprintf(file, "%.4f\n", element)
		}
}


 
func main() {
        var dumpDetection detectionAgent
        dumpDetection.Setup()
        start := time.Now()
        for z := 0; z < 3; z++ {
        for i := 0; i < 600; i++ {
	    dumpDetection.AddStep(float64(i))
	}
        dumpDetection.CloseExperience(int(z),DetectAgentPath) 
        dumpDetection.Clear()
        }    
        elapsed := time.Since(start)
        fmt.Printf("Binomial took %s", elapsed) 
}
