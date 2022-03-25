"""
This function takes in an index 0 - 1024 and maps it to an emoji.
It takes much less ram and storage than listing out all the emojis.
We keep a list of the largest cotinuous emoji sections in unicode,
and use those to map our index.

A seperate helper script is used to create the ranges, and can be
modified to output code for other languages or exclude certain emojis.
"""

def index_to_emoji(i):
    if not (0 <= i < 1024):
        return

    # U+1F400 - U+1F4FC [254]
    if i < 254:
        c = 0x1F400 + (i - 0)

    # U+1F324 - U+1F392 [112]
    elif i < 366:
        c = 0x1F324 + (i - 254)

    # U+1F947 - U+1F9AE [105]
    elif i < 471:
        c = 0x1F947 + (i - 366)

    # U+1F5FA - U+1F64E [86]
    elif i < 557:
        c = 0x1F5FA + (i - 471)

    # U+1F39E - U+1F3EF [83]
    elif i < 640:
        c = 0x1F39E + (i - 557)

    # U+1F9B4 - U+1F9FE [76]
    elif i < 716:
        c = 0x1F9B4 + (i - 640)

    # U+1F680 - U+1F6C4 [70]
    elif i < 786:
        c = 0x1F680 + (i - 716)

    # U+1F4FF - U+1F53C [63]
    elif i < 849:
        c = 0x1F4FF + (i - 786)

    # U+1F90C - U+1F939 [47]
    elif i < 896:
        c = 0x1F90C + (i - 849)

    # U+1F300 - U+1F320 [34]
    elif i < 930:
        c = 0x1F300 + (i - 896)

    # U+1FA90 - U+1FAAB [29]
    elif i < 959:
        c = 0x1FA90 + (i - 930)

    # U+1F550 - U+1F566 [24]
    elif i < 983:
        c = 0x1F550 + (i - 959)

    # U+1F7E0 - U+1F7EA [12]
    elif i < 995:
        c = 0x1F7E0 + (i - 983)

    # U+1FAB0 - U+1FAB9 [11]
    elif i < 1006:
        c = 0x1FAB0 + (i - 995)

    # U+1F191 - U+1F199 [10]
    elif i < 1016:
        c = 0x1F191 + (i - 1006)

    # U+1F6F3 - U+1F6FB [10]
    elif i < 1026:
        c = 0x1F6F3 + (i - 1016)

    return chr(c)
