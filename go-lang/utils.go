package main

import "math/big"

func ToBigBase(value *big.Int, base uint64) (res [](uint64)) {
	toBigBaseImpl(value, base, &res)
	return
}

func toBigBaseImpl(value *big.Int, base uint64, res *[](uint64)) {
	bigBase := new(big.Int).SetUint64(base)
	quotient := new(big.Int).Div(value, bigBase)
	if quotient.Cmp(new(big.Int).SetUint64(0)) != 0 {
		toBigBaseImpl(quotient, base, res)
	}

	*res = append(*res, new(big.Int).Mod(value, bigBase).Uint64())
}
