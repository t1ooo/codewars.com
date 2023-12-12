# https://www.codewars.com/kata/51ba717bb08c1cd60f00002f

# %%

def fmt_range(rng):
    if len(rng) >= 3:
        return f'{rng[0]}-{rng[-1]}'
    return ','.join(map(str, rng))

def solution(a):
    result = []
    rng = []
    for v in a:
        if rng and rng[-1] != v-1:
            result.append(fmt_range(rng))
            rng = []
        rng.append(v)
    result.append(fmt_range(rng))
    return ','.join(result)


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(solution([-6,-3,-2,-1,0,1,3,4,5,7,8,9,10,11,14,15,17,18,19,20]),
                       '-6,-3-1,3-5,7-11,14,15,17-20')
assert_equals(solution([-3,-2,-1,2,10,15,16,18,19,20]),
                       '-3--1,2,10,15,16,18-20')
