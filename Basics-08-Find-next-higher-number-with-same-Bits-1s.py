# https://www.codewars.com/kata/56bdd0aec5dc03d7780010a5

# %%
def next_higher(value):
    n = bin(value).count('1')
    while True:
        value += 1
        if bin(value).count('1') == n:
            return value


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(next_higher(128), 256)
assert_equals(next_higher(1), 2)
assert_equals(next_higher(1022), 1279)
assert_equals(next_higher(127), 191)
assert_equals(next_higher(1253343), 1253359)
