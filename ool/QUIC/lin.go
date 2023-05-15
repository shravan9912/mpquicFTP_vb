package quic
 
import (
	"fmt"
	"os"
)

const banditDimension = 7

var MAaF [banditDimension][banditDimension]float64
var MAaS [banditDimension][banditDimension]float64
var MbaF [banditDimension]float64
var MbaS [banditDimension]float64
 
func main() {
	//os.Remove("/Users/hongjiawu/Documents/bitbuck/mosaic-classification-based-scheduling/MAaF")
	os.Create("/home/shravan/Documents/dronenextwork/new/mpquicFTP_vb/sch_out/lin")
	file2, _ := os.OpenFile("/home/shravan/Documents/dronenextwork/new/mpquicFTP_vb/sch_out/lin", os.O_WRONLY, 0600)
	for i := 0; i < banditDimension; i++ {
		for j := 0; j < banditDimension; j++ {
			if i == j{
				fmt.Fprintf(file2, "%.4f\n", 1.0)
			} else {
				fmt.Fprintf(file2, "%.4f\n", 0.0)
			}
		}
	}
	for i := 0; i < banditDimension; i++ {
		for j := 0; j < banditDimension; j++ {
			if i == j{
				fmt.Fprintf(file2, "%.4f\n", 1.0)
			} else {
				fmt.Fprintf(file2, "%.4f\n", 0.0)
			}
		}
	}
	for i := 0; i < 2; i++ {
		for j := 0; j < banditDimension; j++ {
			if i == j{
				fmt.Fprintf(file2, "%.4f\n", 0.0)
			}
		}
	}
	file2.Close()
	file, err := os.Open("/home/mosaic/edge-computing-mpquic/mmwave/lin")
	if err != nil {
    	panic(err)
	}

	for i := 0; i < banditDimension; i++ {
		for j := 0; j < banditDimension; j++ {
			fmt.Fscanln(file, &MAaF[i][j])
			fmt.Printf("%.4f\n",MAaF[i][j])
		}
	}

	for i := 0; i < banditDimension; i++ {
		for j := 0; j < banditDimension; j++ {
			fmt.Fscanln(file, &MAaS[i][j])
			fmt.Printf("%.4f\n",MAaS[i][j])
		}
	}

	for i := 0; i < banditDimension; i++ {
		fmt.Fscanln(file, &MbaF[i])
		fmt.Printf("%.4f\n",MbaF[i])
	}

	for i := 0; i < banditDimension; i++ {
		fmt.Fscanln(file, &MbaS[i])
		fmt.Printf("%.4f\n",MbaS[i])
	}
	file.Close()
}
