# https://www.codewars.com/kata/52bc74d4ac05d0945d00054e


# %%
from collections import Counter

def first_non_repeating_letter_v1(string):
    string_lower = string.lower()
    c = Counter(string_lower)
    for i,ch in enumerate(string_lower):
        if c[ch] == 1:
            return string[i]
    return ''


def first_non_repeating_letter(string):
    c = Counter(string.lower())
    for ch in string:
        if c[ch.lower()] == 1:
            return ch
    return ''


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(first_non_repeating_letter('a'), 'a')
assert_equals(first_non_repeating_letter('stress'), 't')
assert_equals(first_non_repeating_letter('moonmen'), 'e')


assert_equals(first_non_repeating_letter(''), '')


assert_equals(first_non_repeating_letter('abba'), '')
assert_equals(first_non_repeating_letter('aa'), '')


assert_equals(first_non_repeating_letter('~><#~><'), '#')
assert_equals(first_non_repeating_letter('hello world, eh?'), 'w')


assert_equals(first_non_repeating_letter('sTreSS'), 'T')
assert_equals(first_non_repeating_letter('Go hang a salami, I\'m a lasagna hog!'), ',')
