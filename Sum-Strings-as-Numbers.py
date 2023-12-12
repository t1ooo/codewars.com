# https://www.codewars.com/kata/5324945e2ece5e1f32000370

# %%
divmod(12, 10)

# %%
def sum_strings(x, y):  
    ln = max(len(x), len(y))
    x = x.rjust(ln, '0')
    y = y.rjust(ln, '0')

    digits = []
    d = 0
    for a,b in zip(x[::-1], y[::-1]):
        d, r = divmod(int(a)+int(b)+d, 10)
        digits.append(str(r))
    
    digits.append(str(d)[::-1])
    
    return ''.join(digits).rstrip('0')[::-1] or '0'



def assert_equals(actual, expected, msg=None):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'



assert_equals(sum_strings("1", "1"), "2")
assert_equals(sum_strings("123", "456"), "579")

import random
import sys
for _ in range(10):
    x = random.randint(0, sys.maxsize)
    y = random.randint(0, sys.maxsize)
    z = x+y
    assert_equals(sum_strings('0'+str(x), '0'+str(y)), str(z), (x,y))
