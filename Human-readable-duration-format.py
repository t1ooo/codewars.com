# https://www.codewars.com/kata/52742f58faf5485cae000b9a

import sys

def format_duration(s):
    if s == 0: return 'now'
    data = [
        ['year',   60*60*24*365, sys.maxsize],
        ['day',    60*60*24,     365],
        ['hour',   60*60,        24],
        ['minute', 60,           60],
        ['second', 1,            60]]
    tmp = [f"{n} {name}{'s' if 1 < n else ''}"
           for name, div, rem in data
           if (n := int(s/div)%rem) != 0]
    head, tail = ', '.join(tmp[:-1]), tmp[-1]
    return f'{head} and {tail}' if head else tail


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(format_duration(0), "now")
assert_equals(format_duration(1), "1 second")
assert_equals(format_duration(62), "1 minute and 2 seconds")
assert_equals(format_duration(120), "2 minutes")
assert_equals(format_duration(3600), "1 hour")
assert_equals(format_duration(3662), "1 hour, 1 minute and 2 seconds")
assert_equals(format_duration(132030240), "4 years, 68 days, 3 hours and 4 minutes")
