# https://www.codewars.com/kata/51e056fe544cf36c410000fb

# %%
import re
from collections import Counter

def top_3_words_v1(text):
    matches = [m
               for m in re.findall(r"[a-z']+", text.lower())
               if re.search(r'[a-z]', m)]
    return [w for w,_ in Counter(matches).most_common(3)]


def top_3_words(text):
    matches = re.findall(r"[a-z']*[a-z]+[a-z']*", text.lower())
    return [w for w,_ in Counter(matches).most_common(3)]


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(top_3_words("a a a  b  c c  d d d d  e e e e e"), ["e", "d", "a"])
assert_equals(top_3_words("e e e e DDD ddd DdD: ddd ddd aa aA Aa, bb cc cC e e e"), ["e", "ddd", "aa"])
assert_equals(top_3_words("  //wont won't won't "), ["won't", "wont"])
assert_equals(top_3_words("  , e   .. "), ["e"])
assert_equals(top_3_words("  ...  "), [])
assert_equals(top_3_words("  '  "), [])
assert_equals(top_3_words("  '''  "), [])
assert_equals(top_3_words("""In a village of La Mancha, the name of which I have no desire to call to
mind, there lived not long since one of those gentlemen that keep a lance
in the lance-rack, an old buckler, a lean hack, and a greyhound for
coursing. An olla of rather more beef than mutton, a salad on most
nights, scraps on Saturdays, lentils on Fridays, and a pigeon or so extra
on Sundays, made away with three-quarters of his income."""), ["a", "of", "on"])
assert_equals(top_3_words("s'nvptta'z qcaouvt gpspbig"), ["s'nvptta'z", 'qcaouvt', 'gpspbig'])
