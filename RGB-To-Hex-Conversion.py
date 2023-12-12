# https://www.codewars.com/kata/513e08acc600c94f01000001

# %%
def convert(n):
    n = max(n, 0)
    n = min(n, 255)
    return f'{n:02x}'.upper()

def rgb(r, g, b):
    return ''.join(map(convert, [r,g,b]))


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(rgb(0, 0, 0), "000000", "testing zero values")
assert_equals(rgb(1, 2, 3), "010203", "testing near zero values")
assert_equals(rgb(255, 255, 255), "FFFFFF", "testing max values")
assert_equals(rgb(254, 253, 252), "FEFDFC", "testing near max values")
assert_equals(rgb(-20, 275, 125), "00FF7D", "testing out of range values")
