package main

import (
	"fmt"
	"log"
	"math/big"
	"os"
)

func main() {
	value, _ := new(big.Int).SetString("0x86138b210f21d41c757ae8a5d2a4cb29c1350f73", 0)

	if len(os.Args[1:]) > 0 {
		readValue, ok := new(big.Int).SetString(os.Args[1], 0)
		if !ok {
			log.Fatal("invalid value")
		}
		value = readValue
	}

	emojisAlphabet, err := LoadEmojisAlphabet()
	if err != nil {
		log.Fatal(err)
	}

	emojiHash, err := ToEmojiHash(value, 0, emojisAlphabet)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("emojihash:", emojiHash)

	colorHashAlphabet := MakeColorHashAlphabet(5, 32)
	colorHash := ToColorHash(value, &colorHashAlphabet, 32)

	printColorHash := func() {
		fmt.Print("colorhash: ")
		for _, v := range colorHash {
			fmt.Print("[")
			for i := 0; i < v[0]; i++ {
				fmt.Print(v[1])
				if i != v[0]-1 {
					fmt.Print(" ")
				}
			}
			fmt.Print("]")
		}
		fmt.Println()
	}
	printColorHash()
}
