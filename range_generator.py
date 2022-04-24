import re
import requests

# Fetch a list of all emojis from the unicode org themselves
emoji_test = requests.get("https://unicode.org/Public/emoji/14.0/emoji-test.txt")

# Only grab emojis that are a single character and exclude any "component" emojis
# this excludes the skin and hair modifiers
single_emojis = re.findall(
    r"^(1F...) +; (?:fully-qualified|unqualified|minimally-qualified)",
    emoji_test.text,
    flags=re.I | re.M,
)

single_emojis = [int(e, 16) for e in single_emojis]
single_emojis.sort()

# After parsing as ints, we merge the individual emojis into ranges
ranges = []
start = single_emojis[0]
end = start

for e in single_emojis[1:]:
    # If the current emoji immediately follows the previous, merge them
    if e == end + 1:
        end = e
    else:
        # Only add to the range when we cant merge
        ranges.append((start, end))
        start = e
        end = e
else:
    # Finally add the last range we were working on
    ranges.append((start, end))

# Sort by length of ranges so we can use as few if statements as possible
ranges.sort(key=lambda r:r[0] - r[1])


# Print out code that maps a variable i to a codepoint c
i = 0
for s, e in ranges:
    l = e - s + 1
    print(f"\n# U+{s:X} - U+{e-1:X} [{l}]")
    if i == 0:
        print(f"if i < {i+l}:")
    else:
        print(f"elif i < {i+l}:")
    print(f"    c = 0x{s:X} + (i - {i})")
    i += l

