# emojihash
secure emojihash map for hex strings
```
$ python3 main.py B8B92Cc1Fbe8E425184769B296BAD43245Ad2C84
> 🌙🔕🏒🍝🥁🏟🐽😳🌲🏈🍁🕘👶😠🧸💙
```

go-lang version of emojihash and colorhash (output as sequence of color indexes 0-31)
```
$ cd go-lang
$ go run . 0x86138b210f21d41c757ae8a5d2a4cb29c1350f73
> emojihash: [😅 🦻 ♟️ 🚣🏾‍♀️ 💁🏿 🧏🏾 👨🏾‍🍳]
  colorhash: [3 3][30 30 30 30 30][21 21 21][0 0 0 0][16 16 16 16][4][25 25 25 25 25][19 19 19 19 19][13 13 13][21 21 21]
```
