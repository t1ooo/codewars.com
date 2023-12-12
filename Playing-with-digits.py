# https://www.codewars.com/kata/5552101f47fc5178b1000050

# %%
def dig_pow_v1(n, p):
    digits = list(map(int, str(n)))
    acc = 0
    for digit in digits:
        acc += digit**p
        p+=1
    k = acc/n
    return k if k.is_integer() else -1


def dig_pow(n, p):
    digits = map(int, str(n))
    sum_ = sum(d**(p+i) for i,d in enumerate(digits))
    k = sum_/n
    return k if k.is_integer() else -1


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(dig_pow(89, 1), 1)
assert_equals(dig_pow(92, 1), -1)
assert_equals(dig_pow(46288, 3), 51)
assert_equals(dig_pow(41, 5), 25)
assert_equals(dig_pow(114, 3), 9)
assert_equals(dig_pow(8, 3), 64)
