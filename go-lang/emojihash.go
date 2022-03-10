package main

import (
	"bufio"
	"errors"
	"math/big"
	"os"
	"strings"
)

func ToEmojiHash(value *big.Int, hashLen int, alphabet *[]string) (hash []string, err error) {
	valueBitLen := value.BitLen()
	alphabetLen := new(big.Int).SetInt64(int64(len(*alphabet)))

	indexes := ToBigBase(value, alphabetLen.Uint64())
	if hashLen == 0 {
		hashLen = len(indexes)
	} else if hashLen > len(indexes) {
		prependLen := hashLen - len(indexes)
		for i := 0; i < prependLen; i++ {
			indexes = append([](uint64){0}, indexes...)
		}
	}

	// alphabetLen^hashLen
	possiblePermutations := new(big.Int).Exp(alphabetLen, new(big.Int).SetInt64(int64(hashLen)), nil)

	// 2^valueBitLen
	requiredPermutations := new(big.Int).Exp(new(big.Int).SetInt64(2), new(big.Int).SetInt64(int64(valueBitLen)), nil)

	if possiblePermutations.Cmp(requiredPermutations) == -1 {
		return nil, errors.New("alphabet or hash length is too short to encode given value")
	}

	for _, v := range indexes {
		hash = append(hash, (*alphabet)[v])
	}

	return hash, nil
}

func LoadEmojisAlphabet() (*[]string, error) {
	file, err := os.Open("emojis.txt")
	if err != nil {
		return nil, err
	}

	alphabet := make([]string, 0)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		alphabet = append(alphabet, strings.Replace(scanner.Text(), "\n", "", -1))
	}

	return &alphabet, nil
}
