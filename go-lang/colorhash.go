package main

import "math/big"

func ToColorHash(value *big.Int, alphabet *[][]int, colorsCount int) (hash [][]int) {
	alphabetLen := len(*alphabet)
	indexes := ToBigBase(value, uint64(alphabetLen))
	hash = make([][](int), len(indexes))
	for i, v := range indexes {
		hash[i] = make([](int), 2)
		hash[i][0] = (*alphabet)[v][0]
		hash[i][1] = (*alphabet)[v][1]
	}

	// colors can't repeat themselves
	// this makes color hash not fully collision resistant
	prevColorIdx := hash[0][1]
	hashLen := len(hash)
	for i := 1; i < hashLen; i++ {
		colorIdx := hash[i][1]
		if colorIdx == prevColorIdx {
			hash[i][1] = (colorIdx + 1) % colorsCount
		}
		prevColorIdx = hash[i][1]
	}

	return
}

// [[1 0] [1 1] [1 2] ... [units, colors-1]]
// [3 12] => 3 units length, 12 color index
func MakeColorHashAlphabet(units, colors int) (res [][]int) {
	res = make([][]int, units*colors)
	idx := 0
	for i := 0; i < units; i++ {
		for j := 0; j < colors; j++ {
			res[idx] = make([]int, 2)
			res[idx][0] = i + 1
			res[idx][1] = j
			idx++
		}
	}
	return
}
