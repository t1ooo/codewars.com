# https://www.codewars.com/kata/52597aa56021e91c93000cb0

# %%
def move_zeros_v1(lst):
    non_zeros = []
    zeros = []
    for v in lst:
        (zeros if v == 0 else non_zeros).append(v)
    return non_zeros + zeros


def move_zeros(lst):
    i = 0
    ln = len(lst)
    while i < ln:
        if lst[i] == 0:
            lst[i:ln-1] = lst[i+1:ln] # move i <- i+1
            lst[ln-1] = 0 # set last to 0
            ln-=1
        if lst[i] != 0:
            i+=1
    return lst


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(move_zeros(
[1, 2, 0, 1, 0, 1, 0, 3, 0, 1]),
[1, 2, 1, 1, 3, 1, 0, 0, 0, 0])
assert_equals(move_zeros(
[9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9]),
[9, 9, 1, 2, 1, 1, 3, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
assert_equals(move_zeros([0, 0]), [0, 0])
assert_equals(move_zeros([0]), [0])
assert_equals(move_zeros([]), [])


# lst = [1, 2, 0, 1, 0, 1, 0, 3, 0, 1]
# %timeit move_zeros_v1(lst) # 1.22 µs ± 128 ns per loop
# %timeit move_zeros(lst) # 2.57 µs ± 109 ns per loop
