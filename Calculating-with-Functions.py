# https://www.codewars.com/kata/525f3eda17c7cd9f9e000b39

# %%
stack = [2, 'divided_by', 6]
right, op, left = stack
if op == 'divided_by':
    print(int(left / right))

# %%

def calc(s):
    left, op, right = s
    if op == '+': return right + left
    if op == '-': return right - left
    if op == '*': return right * left
    if op == '/': return int(right / left)

def helper(arg, s=None):
    s = (s or []) + [arg]
    return calc(s) if len(s) == 3 else s

def zero(s=None)  : return helper(0, s)
def one(s=None)   : return helper(1, s)
def two(s=None)   : return helper(2, s)
def three(s=None) : return helper(3, s)
def four(s=None)  : return helper(4, s)
def five(s=None)  : return helper(5, s)
def six(s=None)   : return helper(6, s)
def seven(s=None) : return helper(7, s)
def eight(s=None) : return helper(8, s)
def nine(s=None)  : return helper(9, s)

def plus(s)       : return helper('+', s)
def minus(s)      : return helper('-', s)
def times(s)      : return helper('*', s)
def divided_by(s) : return helper('/', s)


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(seven(times(five())), 35)
assert_equals(four(plus(nine())), 13)
assert_equals(eight(minus(three())), 5)
assert_equals(six(divided_by(two())), 3)
