package main

import (
	"reflect"
	"testing"
)

func TestColorHash(t *testing.T) {
	alphabet := MakeColorHashAlphabet(4, 4)

	checker := func(valueStr string, expected *[][](int)) {
		value := toBigInt(t, valueStr)
		res := ToColorHash(value, &alphabet, 4)
		if !reflect.DeepEqual(res, *expected) {
			t.Fatalf("invalid colorhash conversion %v != %v", res, *expected)
		}
	}

	checker("0x0", &[][]int{{1, 0}})
	checker("0x1", &[][]int{{1, 1}})
	checker("0x4", &[][]int{{2, 0}})
	checker("0xF", &[][]int{{4, 3}})

	// oops, collision
	checker("0xFF", &[][]int{{4, 3}, {4, 0}})
	checker("0xFC", &[][]int{{4, 3}, {4, 0}})

	checker("0xFFFF", &[][]int{{4, 3}, {4, 0}, {4, 3}, {4, 0}})
}
