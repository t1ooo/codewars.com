# https://www.codewars.com/kata/545cedaa9943f7fe7b000048

# %%
import string


def is_pangram_v1(s):
    s = s.lower()
    return all(ch in s for ch in string.ascii_lowercase)

def is_pangram(s):
    return set(string.ascii_lowercase) \
        .issubset(set(s.lower()))


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(is_pangram(
    "The quick, brown fox jumps over the lazy dog!"), True)
assert_equals(is_pangram("1bcdefghijklmnopqrstuvwxyz"), False)
