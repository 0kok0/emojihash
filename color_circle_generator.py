from math import comb, perm


def circle_count(circle_slices: int, circle_segments: int, colors: int):
    # First we count the ways we can distribute the slices among the segments
    # with each segment having at least 1 slice
    partitions = comb(circle_slices - 1, circle_segments - 1)

    # Then how many ways we can color the segments uniquely
    colorings = perm(colors, circle_segments)

    return (partitions, colorings)

def compress_digits(digits, bases):
    """ Turns a set of digits and their bases into a single number """
    n = 0
    for digit, base in zip(digits[::-1], bases[::-1]):
        n = (n * base) + digit
    return n

def extract_digits(n, bases):
    """ Turns a number into a set of digits given a list of bases """
    digits = []
    for base in bases:
        n, digit = divmod(n, base)
        digits.append(digit)
    return digits

def generate_ranges(slices: int, max_segments: int, colors: int):
    i = 0
    for K in range(1, max_segments + 1):
        partitions, colorings = circle_count(slices, K, colors)
        count = partitions * colorings
        bases = [partitions]
        for n in range(colors, colors - K, -1):
            bases.append(n)

        print(f"# {K} segments")
        print(f"if i < {i + count}:")
        print(f"    return extract(i - {i}, {slices}, {K}, {bases})")
        i += count

if __name__ == '__main__':
    generate_ranges(10, 10, 16)

