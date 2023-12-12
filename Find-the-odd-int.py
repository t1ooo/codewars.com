# https://www.codewars.com/kata/54da5a58ea159efa38000836

# %%
assert 1^1 == 0
assert 1^99^1 == 99
assert 2^1^99^1^2 == 99

# %%
from collections import Counter

def find_it_v1(seq):
    for n, count in Counter(seq).items():
        if count%2==1:
            return n
    return None


# 1^1 == 0
# 1^99^1 == 99
# 2^1^99^1^2 == 99
def find_it(xs):
    acc = 0
    for x in xs:
        acc = acc^x
    return acc


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(find_it([20,1,-1,2,-2,3,3,5,5,1,2,4,20,4,-1,-2,5]), 5)
assert_equals(find_it([1,1,2,-2,5,2,4,4,-1,-2,5]), -1);
assert_equals(find_it([20,1,1,2,2,3,3,5,5,4,20,4,5]), 5);
assert_equals(find_it([10]), 10);
assert_equals(find_it([10, 10, 10]), 10);        
assert_equals(find_it([1,1,1,1,1,1,10,1,1,1,1]), 10);
assert_equals(find_it([5,4,3,2,1,5,4,3,2,10,10]), 1);
