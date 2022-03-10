package main

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestToEmojiHash(t *testing.T) {
	alphabet := [](string){"😇", "🤐", "🥵", "🙊", "🤌"}

	checker := func(valueStr string, hashLen int, expected *[](string)) {
		value := toBigInt(t, valueStr)
		res, err := ToEmojiHash(value, hashLen, &alphabet)
		require.NoError(t, err)
		if !reflect.DeepEqual(res, *expected) {
			t.Fatalf("invalid emojihash conversion %v != %v", res, *expected)
		}
	}

	checker("777", 5, &[](string){"🤐", "🤐", "🤐", "😇", "🥵"})
	checker("777", 0, &[](string){"🤐", "🤐", "🤐", "😇", "🥵"})
	checker("777", 10, &[](string){"😇", "😇", "😇", "😇", "😇", "🤐", "🤐", "🤐", "😇", "🥵"})

	// 20bytes of data described by 14 emojis requires at least 2757 length alphabet
	alphabet = make([](string), 2757)
	val := toBigInt(t, "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF") // 20 bytes
	_, err := ToEmojiHash(val, 14, &alphabet)
	require.NoError(t, err)

	alphabet = make([](string), 2757-1)
	_, err = ToEmojiHash(val, 14, &alphabet)
	require.Error(t, err)
}
