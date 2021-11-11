import json
import math
import sys

"""
PoC script for an emoji_hasher. On a high level, we define a _bijective/collision resistant_ map from the 
arbitrary length binary alphabet {0,1}^* ->  {😳....😠}^* to a subset of a unicode emoji alphabet. 
-   TODO: Implementation assumes hex strings, could be generalized 
-   The image alphabet MUST contain a subset of size 2^n s.t. the map can operate on n bits. 
    If this constraint is violated, the map is not collision resistant. 
-   The emoji_hash can be used for compression; 
    given an emoji alphabet size of 2**10, hex strings are compressed by ~ 60% 
-   The emoji_hash depends on the order of the image alphabet. Therefore, the image alphabet MUST be 
    hardcoded/securely distributed with the application generating/verifying hashes 
"""

# random eth address 20 byte length sample, works with any hex string
key_string: str = sys.argv[1] if len(sys.argv) > 1 else "B8B92Cc1Fbe8E425184769B296BAD43245Ad2C84"

emoji_alphabet_path = sys.argv[2] if len(sys.argv) > 2 else "all_emojis.json"

with open(emoji_alphabet_path) as f:
    all_emojis: dict = json.load(f)


def string_to_emoji_hash(
    hex_string: str, alphabet_size: int = 10, emoji_alphabet: dict[int, str] = None
) -> str:
    # we need to operate on bits to support arbitrary image alphabet sizes (2**10 by default)
    key_bits: str = bin(int(hex_string, 16))
    key_bits = key_bits.removeprefix("0b")

    if emoji_alphabet is None:
        # we filter some insecure/unwanted emoji mutations (skin tones, combinations, flags)
        emoji_alphabet = filter_emoji_alphabet(all_emojis)

    # verify some properties the alphabet needs to have

    # no duplicate characters
    assert len(emoji_alphabet) == len(set(emoji_alphabet))

    # there MUST be enough chars in the alphabet to define a bijective/collision resistant map to a subset thereof
    assert 2 ** alphabet_size <= len(emoji_alphabet)

    emoji_hash: str = str()
    # Using ceil here to iterate over remainder if string is less than full alphabet size.
    for index in range(math.ceil(len(key_bits) / alphabet_size)):
        # Iterating over chunks of key string in <alphabet_size> bits.
        segment: str = key_bits[
            index * alphabet_size: index * alphabet_size + alphabet_size
        ]
        # Converting bits back to number for indexing/key.
        emoji_index: int = int(segment, 2)
        # Mapping to emoji:
        emoji: str = emoji_alphabet[emoji_index]
        emoji_hash += emoji
    return emoji_hash


def filter_emoji_alphabet(emoji_alphabet: dict) -> dict[int, str]:
    filtered_emojis: dict = dict()
    index = 0
    for char in emoji_alphabet:
        # filter skin tone, as visually hard to distinguish for the user
        if "skin tone" in char["name"]:
            continue
        # filter emoji combinations and some misc
        if len(char["characters"]) > 1:
            continue
        filtered_emojis[index] = char["characters"]
        index = index + 1
    return filtered_emojis


result: str = string_to_emoji_hash(key_string)
print(result)
