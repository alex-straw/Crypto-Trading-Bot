import bisect


def bisect_left_rev(a, x, lo=0, hi=None):
    """ For descending array """
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] > x: lo = mid+1
        else: hi = mid
    return lo


def find_closest_index(a, x):
    """ For ascending array """
    i = bisect.bisect_left(a, x)
    if i >= len(a):
        i = len(a) - 1
    elif i and a[i] - x > x - a[i - 1]:
        i = i - 1
    return (i)


def find_closest_index_rev(a, x):
    """ For descending array """
    i = bisect_left_rev(a, x)
    if i >= len(a):
        i = len(a) - 1
    elif i and a[i] - x < x - a[i - 1]:
        i = i - 1
    return (i)