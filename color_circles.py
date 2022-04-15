import math
import random
from math import factorial as fac, comb, perm
from itertools import groupby
from dataclasses import dataclass


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


def extract(index, range_data, N, color_count):
    K = range_data.segments
    max_index = range_data.max_index
    count = range_data.range

    bases = [range_data.partitions]
    for n in range(color_count, color_count - K, -1):
        bases.append(n)

    # The bases are arranged [partition base, color 1, color 2, ...]
    [partition, *colors] = extract_digits(index, bases)
    # Now we go from partition index to segment lengths.
    segments = [s + 1 for s in star_bars_unrank(partition, N - K, K - 1)]
    return (tuple(segments), tuple(adjust_colors(colors)))


def circle_count(circle_slices: int, circle_segments: int, colors: int):
    # First we count the ways we can distribute the slices among the segments
    # with each segment having at least 1 slice
    partitions = comb(circle_slices - 1, circle_segments - 1)

    # Then how many ways we can color the segments uniquely
    colorings = perm(colors, circle_segments)

    return (partitions, colorings)


@dataclass
class CircleRange:
    max_index: int
    range: int
    partitions: int
    segments: int

def generate_ranges(slices: int, max_segments: int, colors: int):
    circle_ranges = []

    i = 0
    for K in range(1, max_segments + 1):
        partitions, colorings = circle_count(slices, K, colors)
        count = partitions * colorings

        circle_ranges.append(CircleRange(
          max_index = i + count,
          range = count,
          partitions = partitions,
          segments = K,
        ))
        i += count

    return circle_ranges


def index_to_circle(index, circle_ranges, pieces, color_count):
    range_i = 0
    while index >= circle_ranges[range_i].max_index:
        range_i += 1

    circle_range = circle_ranges[range_i]
    offset = circle_range.max_index - circle_range.range

    return extract(
        index - offset,
        circle_range,
        pieces,
        color_count
    )

if __name__ == '__main__':
    N = 6 # pieces of the circle
    P = 6 # segments to group pieces into
    C = 8 # number of colors we have to color the segments

    circle_ranges = generate_ranges(N, P, C)
    print(f'Total circles: {circle_ranges[-1].max_index}')
    for r in circle_ranges:
        start = r.max_index - r.range
        stop = r.max_index - 1
        print(index_to_circle(start, circle_ranges, N, C))
        print(index_to_circle(stop, circle_ranges, N, C))

    max_i = min(circle_ranges[-1].max_index, 100000)

    all_circles = set()
    for i in range(max_i):
        all_circles.add(index_to_circle(i, circle_ranges, N, C))

    print(len(all_circles), max_i)
