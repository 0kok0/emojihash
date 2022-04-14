import math
import random
from math import factorial as fac, comb
from itertools import groupby


def extract_digits(n, bases):
    """ Turns a number into a set of digits given a list of bases """
    digits = []
    for base in bases:
        n, digit = divmod(n, base)
        digits.append(digit)
    return digits


# https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)
def star_bars_count(s, b):
    """ Determines the number of permutations for this star and bar configuration """
    return comb(s + b, b)


def star_bars_unrank(rank, stars, bars, groups=None):
    """
    Determine the group counts associated with the rank
    for a given star and bar configuration.
    Based off of perm_unrank from https://codegolf.stackexchange.com/a/115024

    It works by building up the star and bar permutation by choosing either
    a star or a bar to add. We remove the string representation of the
    permutation here and just store the group counts that correspond to the
    particular star and bar arrangement.
    i.e. **||*| = [2, 0, 1, 0]
    """
    if groups == None:
        groups = [0]

    # Return if we only have one choice left
    if stars == 0 or bars == 0:
        while bars > 0:
            groups.append(0)
            bars -= 1

        while stars > 0:
            groups[-1] += 1
            stars -= 1

        return groups

    # Possible arrangements if we remove 1 star
    star_count = star_bars_count(stars - 1, bars)

    # We're adding a star, so the last group increments
    if star_count > rank:
        groups[-1] += 1
        return star_bars_unrank(rank, stars - 1, bars, groups)

    # Possible arrangements if we remove 1 bar
    bar_count = star_bars_count(stars, bars - 1)

    # We're adding a bar, so we're adding a new group
    if (star_count + bar_count) > rank:
        groups.append(0)
        return star_bars_unrank(rank - star_count, stars, bars - 1, groups)


def adjust_colors(colors):
    """
    The original color index list needs to be processed so that each
    index is in reference to the entire list of colors. Before processing
    each subsequent index assumes the previous color was removed.

    This way 0,0,0 becomes 0,1,2 because the second and third 0 are indexed
    assuming the previous 0's are popped off. So when the are inserted back
    in, the seconds 0's become 1 and 2 respectively.
    """
    adjusted = []
    for i, c in enumerate(colors):
        # A color index needs to be incremented as many times as there are
        # colors that were used before it that were at a lower index than it
        adjusted.append(c + sum(c >= o for o in colors[:i]))
    return adjusted


def extract(index, N, K, bases):
    # The bases are arranged [partition base, color 1, color 2, ...]
    [partition, *colors] = extract_digits(index, bases)
    # Now we go from partition index to segment lengths
    segments = [s + 1 for s in star_bars_unrank(partition, N - K, K - 1)]
    return (segments, adjust_colors(colors))


def index_to_circle(i):
    """
    Returns a tuple of circle segments lengths and colors based on an integer
    between 0 and 309686528177530816.
    """
    # 1 segments
    if i < 16:
        return extract(i - 0, 30, 1, [1, 16])
    # 2 segments
    if i < 6976:
        return extract(i - 16, 30, 2, [29, 16, 15])
    # 3 segments
    if i < 1371136:
        return extract(i - 6976, 30, 3, [406, 16, 15, 14])
    # 4 segments
    if i < 160977856:
        return extract(i - 1371136, 30, 4, [3654, 16, 15, 14, 13])
    # 5 segments
    if i < 12610302016:
        return extract(i - 160977856, 30, 5, [23751, 16, 15, 14, 13, 12])
    # 6 segments
    if i < 697323130816:
        return extract(i - 12610302016, 30, 6, [118755, 16, 15, 14, 13, 12, 11])
    # 7 segments
    if i < 28085836282816:
        return extract(i - 697323130816, 30, 7, [475020, 16, 15, 14, 13, 12, 11, 10])
    # 8 segments
    if i < 838003296634816:
        return extract(i - 28085836282816, 30, 8, [1560780, 16, 15, 14, 13, 12, 11, 10, 9])
    # 9 segments
    if i < 18656187424378816:
        return extract(i - 838003296634816, 30, 9, [4292145, 16, 15, 14, 13, 12, 11, 10, 9, 8])
    # 10 segments
    if i < 309686528177530816:
        return extract(i - 18656187424378816, 30, 10, [10015005, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7])

if __name__ == '__main__':
    print(index_to_circle(0))
    print(index_to_circle(15))

    print(index_to_circle(16))
    print(index_to_circle(6975))

    print(index_to_circle(6976))
    print(index_to_circle(1371135))

    print(index_to_circle(1371136))
    print(index_to_circle(160977855))

    print(index_to_circle(160977856))
    print(index_to_circle(12610302015))

    print(index_to_circle(12610302016))
    print(index_to_circle(697323130815))

    print(index_to_circle(697323130816))
    print(index_to_circle(28085836282815))

    print(index_to_circle(28085836282816))
    print(index_to_circle(838003296634815))

    print(index_to_circle(838003296634816))
    print(index_to_circle(18656187424378815))

    print(index_to_circle(18656187424378816))
    print(index_to_circle(309686528177530815))
