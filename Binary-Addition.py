# https://www.codewars.com/kata/551f37452ff852b7bd000139

# %%
def add_binary(a,b):
    return f'{a+b:b}'


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(add_binary(1,1),"10")
assert_equals(add_binary(0,1),"1")
assert_equals(add_binary(1,0),"1")
assert_equals(add_binary(2,2),"100")
assert_equals(add_binary(51,12),"111111")
