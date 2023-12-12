# https://www.codewars.com/kata/52685f7382004e774f0001f7


# %%
def make_readable_v1(seconds):
    result = []
    for v in [60*60, 60, 1]:
        n = int(seconds / v)
        result.append(f'{n:02d}')
        seconds = seconds-n*v
    return ':'.join(result)


def make_readable(seconds):
    h = int(seconds / (60 * 60))
    m = int((seconds / 60) % 60)
    s = int(seconds % 60)
    return f'{h:02d}:{m:02d}:{s:02d}'


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(make_readable(0), "00:00:00")
assert_equals(make_readable(5), "00:00:05")
assert_equals(make_readable(60), "00:01:00")
assert_equals(make_readable(86399), "23:59:59")
assert_equals(make_readable(359999), "99:59:59")
