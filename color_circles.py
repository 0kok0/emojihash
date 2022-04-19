from math import factorial as fac, comb, perm
from dataclasses import dataclass
from typing import Iterable, Tuple
import time


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


def adjust_colors(colors, color_count):
    """
    The original color index list needs to be processed so that each
    index is in reference to the entire list of colors. Before processing
    each subsequent index assumes the previous color was removed.

    This way 0,0,0 becomes 0,1,2 because the second and third 0 are indexed
    assuming the previous 0's are popped off. So when the are inserted back
    in, the seconds 0's become 1 and 2 respectively.
    """

    indexes = list(range(color_count))
    adjusted = [indexes.pop(c) for c in colors]

    return adjusted


def extract(index, range_data, N, color_count):
    K = range_data.segments

    bases = [range_data.partitions]
    for n in range(color_count, color_count - K, -1):
        bases.append(n)

    # The bases are arranged [partition base, color 1, color 2, ...]
    [partition, *colors] = extract_digits(index, bases)
    # Now we go from partition index to segment lengths.
    segments = [s + 1 for s in star_bars_unrank(partition, N - K, K - 1)]
    return (tuple(segments), tuple(adjust_colors(colors, color_count)))


def circle_count(circle_pieces: int, circle_segments: int, colors: int):
    # First we count the ways we can distribute the pieces among the segments
    # with each segment having at least 1 slice
    partitions = comb(circle_pieces - 1, circle_segments - 1)

    # Then how many ways we can color the segments uniquely
    colorings = perm(colors, circle_segments)

    return (partitions, colorings)


@dataclass
class CircleRange:
    min_index: int
    max_index: int
    size: int
    partitions: int
    segments: int


class ColoredCircles:
    """
    Class to map indexes to uniquely colored and segmented circles.

    Circles are split into pieces which then get merged into segments which
    are then uniquely colored.

    circle_pieces: The number of pieces the overall circle is split up into.
    allowable_segment_counts: A list of segment counts that we want to allow
        circles to group the pieces into. For instance, [1, 2, 3] will allow
        indexes to map to circles that have 1, 2, or 3 segments made from the
        circle pieces.
    color_count: How many colors are available to color the segments.
    """
    def __init__(self, circle_pieces: int, allowable_segment_counts: Iterable[int], color_count: int):
        self.pieces = circle_pieces
        self.color_count = color_count
        self.ranges = []

        i = 0
        for K in allowable_segment_counts:
            partitions, colorings = circle_count(self.pieces, K, color_count)
            count = partitions * colorings

            self.ranges.append(CircleRange(
              min_index = i,
              max_index = i + count - 1,
              size = count,
              partitions = partitions,
              segments = K,
            ))
            i += count

        self.total_circles = self.ranges[-1].max_index + 1

    def index_to_circle(self, index: int) -> Tuple[Tuple[int], Tuple[int]]:
        """
        Given an index, returns a tuple of segment lengths and segment colors.
        The segment lengths sum up to the circle_pieces specified in the
        constructor. And the colors are indexes up to the color_count specified.

        Ex. A return value of ((1,2,3), (0, 2, 1)) describes a circle where the
        first segment is made up of 1 circle piece and is the 0th color. The
        second segment has 2 pieces and is the 2nd color. The third segment has
        3 pieces and is the 1st color.
        """
        if not (0 <= index <= self.ranges[-1].max_index):
            raise ValueError(f"The index {index} is out of range")

        range_i = 0
        while index > self.ranges[range_i].max_index:
            range_i += 1

        circle_range = self.ranges[range_i]
        offset = circle_range.max_index - circle_range.size + 1

        return extract(
            index - offset,
            circle_range,
            self.pieces,
            self.color_count
        )
        

if __name__ == '__main__':
    N = 6 # pieces of the circle
    P = 6 # segments to group pieces into
    C = 8 # number of colors we have to color the segments

    colored_circles = ColoredCircles(N, range(1, P + 1), C)

    print(f'Total circles: {colored_circles.total_circles}')
    for r in colored_circles.ranges:
        start = r.max_index - r.size + 1
        stop = r.max_index
        print(colored_circles.index_to_circle(start))
        print(colored_circles.index_to_circle(stop))

    
    all_circles = set()
    expected_length = min(colored_circles.total_circles, 100000)

    start_time = time.time()
    for i in range(expected_length):
        all_circles.add(colored_circles.index_to_circle(i))
    stop_time = time.time()

    assert(len(all_circles) == expected_length)
    print(f"{expected_length} unique circle arrangments were generated correctly")
    print(f"{(stop_time - start_time) / expected_length * 1000000:.3f} us per circle generation")

    try:
        all_circles.add(colored_circles.index_to_circle(-1))
    except ValueError as e:
        print(e)

    try:
        all_circles.add(colored_circles.index_to_circle(colored_circles.total_circles))
    except ValueError as e:
        print(e)
