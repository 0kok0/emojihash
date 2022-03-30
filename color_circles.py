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
    unranked = perm_unrank(partition, '*' * N + '|' * (K - 1))
    segments = [len(s) + 1 for s in unranked.split('|')]
    return (segments, adjust_colors(colors))


def index_to_circle(i):
    """
    Returns a tuple of circle segments lengths and colors based on an integer
    between 0 and 90742178176.
    """
    # 1 segments
    if i < 16:
        return extract(i - 0, 10, 1, [1, 16])
    # 2 segments
    if i < 2176:
        return extract(i - 16, 10, 2, [9, 16, 15])
    # 3 segments
    if i < 123136:
        return extract(i - 2176, 10, 3, [36, 16, 15, 14])
    # 4 segments
    if i < 3792256:
        return extract(i - 123136, 10, 4, [84, 16, 15, 14, 13])
    # 5 segments
    if i < 69836416:
        return extract(i - 3792256, 10, 5, [126, 16, 15, 14, 13, 12])
    # 6 segments
    if i < 796322176:
        return extract(i - 69836416, 10, 6, [126, 16, 15, 14, 13, 12, 11])
    # 7 segments
    if i < 5639560576:
        return extract(i - 796322176, 10, 7, [84, 16, 15, 14, 13, 12, 11, 10])
    # 8 segments
    if i < 24320622976:
        return extract(i - 5639560576, 10, 8, [36, 16, 15, 14, 13, 12, 11, 10, 9])
    # 9 segments
    if i < 61682747776:
        return extract(i - 24320622976, 10, 9, [9, 16, 15, 14, 13, 12, 11, 10, 9, 8])
    # 10 segments
    if i < 90742178176:
        return extract(i - 61682747776, 10, 10, [1, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7])

