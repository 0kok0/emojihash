import math
import random
from math import factorial as fac
from itertools import groupby


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

# Perm functions from https://codegolf.stackexchange.com/a/115024 and likely
# can be made more efficient by making them less general

def perm_count(s):
    """Count the total number of permutations of sorted sequence `s`"""
    n = fac(len(s))
    for _, g in groupby(s):
        n //= fac(sum(1 for u in g))
    return n

def perm_rank(target, base):
    """Determine the permutation rank of string `target`
    given the rank zero permutation string `base`,
    i.e., the chars in `base` are in lexicographic order.
    """
    if len(target) < 2:
        return 0
    total = 0
    head, newtarget = target[0], target[1:]
    for i, c in enumerate(base):
        newbase = base[:i] + base[i + 1 :]
        if c == head:
            return total + perm_rank(newtarget, newbase)
        elif i and c == base[i - 1]:
            continue
        total += perm_count(newbase)

def perm_unrank(rank, base, head=''):
    ''' Determine the permutation with given rank of the 
        rank zero permutation string `base`.
    '''
    if len(base) < 2:
        return head + ''.join(base)

    total = 0
    for i, c in enumerate(base):
        if i < 1 or c != base[i-1]:
            newbase = base[:i] + base[i+1:]
            newtotal = total + perm_count(newbase)
            if newtotal > rank:
                return perm_unrank(rank - total, newbase, head + c)
            total = newtotal

def adjust_colors(colors):
    """
    The original color index list needs to be processed so that each
    index is in reference to the entire list of colors. Before processing
    each subsequent index assumes the previous color was removed.
    """
    adjusted = []
    for i, c in enumerate(colors):
        adjusted.append(c + sum(c >= o for o in colors[:i]))
    return adjusted

def extract(index, N, K, bases):
    # The bases are arranged [partition base, color 1, color 2, ...]
    [partition, *colors] = extract_digits(index, bases)
    # Now we go from partition index to segment lengths. I think this part could be made more efficient
    unranked = perm_unrank(partition, '*' * (N - K) + '|' * (K - 1))
    segments = [len(s) + 1 for s in unranked.split('|')]
    return (segments, adjust_colors(colors))


def index_to_circle(i):
    """
    Returns a tuple of circle segments lengths and colors based on an integer
    between 0 and 90742178176.
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


def polar_to_xy(cx, cy, radius, angle_rad):
    x = cx + radius * math.cos(angle_rad)
    y = cy + radius * math.sin(angle_rad)

    return x, y

def make_arc(x, y, radius, start_angle, end_angle):
    startx,starty = polar_to_xy(x, y, radius, end_angle)
    endx,endy = polar_to_xy(x, y, radius, start_angle)

    large_arc_flag = (end_angle - start_angle) > math.pi
    #sweep_flag = end_angle > start_angle ? 0 : 1; //sic

    move = f'M {startx:.4f},{starty:.4f} '
    arc = f'A {radius:.4f},{radius:.4f} 0 {int(large_arc_flag)} 0 {endx:.4f},{endy:.4f}'

    return move + arc

def circle_to_svg(segments, colors):
    COLOR_LIST = [
        '#ff0000', '#ffa3a3', # red
        '#ffa100', '#ffdda3', # orange
        '#24db00', '#b3eaa9', # green
        '#00ebac', '#b9fae9', # teal
        '#00b2ff', '#70d4ff', # cyan
        '#0045e5', '#819fe5', # blue
        '#5c0aff', '#b18aff', # purple
        '#c00ddb', '#f08fff', # pink
    ]

    angles = [0.0]
    total_segment = sum(segments)
    segment_start = 0
    for s in segments:
        segment_start += s
        angles.append(segment_start / total_segment * math.tau)

    paths = []
    for i, col in enumerate(colors):
        d = make_arc(0, 0, 100, angles[i], angles[i+1])
        path = f'<path d="{d}" fill="none" stroke="{COLOR_LIST[col]}" stroke-width="30" />'
        paths.append(path)

    return f'<svg width="100px" version="1.1" viewBox="-120 -120 240 240" xmlns="http://www.w3.org/2000/svg">{"".join(paths)}</svg>'

def index_to_svg(i):
    return circle_to_svg(*index_to_circle(i))

if __name__ == '__main__':
    #print(index_to_svg(912423234))
    print(''.join(index_to_svg(random.randint(0, 309686528177530816)) for _ in range(256)))
