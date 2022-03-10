package main

import (
	"math"
	"math/big"
	"reflect"
	"testing"
)

func TestToBigBase(t *testing.T) {
	checker := func(value *big.Int, base uint64, expected *[](uint64)) {
		res := ToBigBase(value, base)
		if !reflect.DeepEqual(res, *expected) {
			t.Fatalf("invalid big base conversion %v != %v", res, *expected)
		}
	}

	lengthChecker := func(value *big.Int, base, expectedLength uint64) {
		res := ToBigBase(value, base)
		if len(res) != int(expectedLength) {
			t.Fatalf("invalid big base conversion %d != %d", len(res), expectedLength)
		}
	}

	checker(new(big.Int).SetUint64(15), 16, &[](uint64){15})
	checker(new(big.Int).SetUint64(495), 16, &[](uint64){1, 14, 15})
	checker(new(big.Int).SetUint64(495), 30, &[](uint64){16, 15})
	checker(new(big.Int).SetUint64(495), 1024, &[](uint64){495})
	checker(new(big.Int).SetUint64(2048), 1024, &[](uint64){2, 0})

	base := uint64(math.Pow(2, 7*4))
	checker(toBigInt(t, "0xFFFFFFFFFFFFFF"), base, &[](uint64){base - 1, base - 1})

	val := toBigInt(t, "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
	lengthChecker(val, 2757, 14)
	lengthChecker(val, 2756, 15)
}

func toBigInt(t *testing.T, str string) *big.Int {
	res, ok := new(big.Int).SetString(str, 0)
	if !ok {
		t.Errorf("invalid conversion to int from %s", str)
	}
	return res
}
