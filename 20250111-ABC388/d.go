package main

import (
	"fmt"
)

func main() {
	var N int
	fmt.Scan(&N)

	A := make([]int, N)
	for i := 0; i < N; i++ {
		fmt.Scan(&A[i])
	}
	
	for n := 1; n < N; n++ {
		count := 0
		for m := 0; m < n; m++ {
			if A[m] > 0 {
				count++
			}
		}

		A[n] += count

		for m := 0; m < n; m++ {
			if A[m] > 0 {
				A[m]--
			}
		}
	}

	for i := 0; i < N; i++ {
		fmt.Printf("%d ", A[i])
	}
}
