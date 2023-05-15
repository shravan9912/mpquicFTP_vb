package quic
 
import (
	"fmt"
	"os"
)

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

