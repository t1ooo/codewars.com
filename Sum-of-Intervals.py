# https://www.codewars.com/kata/52b7ed099cdc285c300001cd

# %%
def sum_of_intervals_v1(intervals):
    intervals.sort(key=lambda x: x[0])

    intr = intervals[0]
    s = abs(intr[1] - intr[0])
    last = intr[1]
    del intervals[0]

    while len(intervals) > 0:
        for i, intr in enumerate(intervals):
            if intr[0] <= last and intr[1] <= last:
                del intervals[i]
                break
            if intr[0] <= last:
                s += abs(intr[1] - last)
                last = intr[1]
                del intervals[i]
                break
            if last <= intr[0]:
                s += abs(intr[1] - intr[0])
                last = intr[1]
                del intervals[i]
                break
    return s


def sum_of_intervals(intervals):
    intervals.sort(key=lambda x: x[0])

    a, b = intervals[0]
    s = b - a
    last = b

    for a, b in intervals:
        if a <= last <= b:
            s += b - last
            last = b
        elif last <= a:
            s += b - a
            last = b

    return s


# TEST
def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(sum_of_intervals([(1, 5)]), 4)
assert_equals(sum_of_intervals([(1, 5), (6, 10)]), 8)
assert_equals(sum_of_intervals([(1, 5), (1, 5)]), 4)
assert_equals(sum_of_intervals([(1, 4), (7, 10), (3, 5)]), 7)
assert_equals(sum_of_intervals(
    [(-1_000_000_000, 1_000_000_000)]), 2_000_000_000)
assert_equals(sum_of_intervals(
    [(0, 20), (-100_000_000, 10), (30, 40)]), 100_000_030)
assert_equals(sum_of_intervals(
    [(409, 475), (-255, -70), (170, 275), (-48, 279), (472, 484)]), 587)
assert_equals(sum_of_intervals(
    [(-49, 455), (488, 495), (-449, -204), (-44, 451), (-341, 499), (480, 481), (200, 231)]), 948)
assert_equals(sum_of_intervals(
    [(16, 105), (-297, -296), (272, 357), (-347, -189), (88, 310)]), 499)
