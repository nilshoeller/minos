package lib

import "math/rand"

// performMatrixMultiplication performs a basic matrix multiplication.
// For demonstration purposes, it multiplies two 100x100 matrices.
func performMatrixMultiplication() {
	size := 500
	a := make([][]int, size)
	b := make([][]int, size)
	result := make([][]int, size)

	for i := range a {
		a[i] = make([]int, size)
		b[i] = make([]int, size)
		result[i] = make([]int, size)
		for j := range a[i] {
			a[i][j] = rand.Intn(100)
			b[i][j] = rand.Intn(100)
		}
	}

	// Matrix multiplication
	for i := 0; i < size; i++ {
		for j := 0; j < size; j++ {
			for k := 0; k < size; k++ {
				result[i][j] += a[i][k] * b[k][j]
			}
		}
	}
}
