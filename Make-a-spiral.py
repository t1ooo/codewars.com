# https://www.codewars.com/kata/534e01fbbb17187c7e0000c6

#%%
from itertools import cycle

def spiralize(size):
    spiral = [[0]*size for _ in range(size)]
    diff = cycle([[0, 1], [1, 0], [0, -1], [-1, 0]])

    def value(x, y):
        return spiral[x][y] if (0<=x < size and 0 <= y < size) else None
    
    dx, dy = next(diff)
    x, y = 0, 0
    spiral[x][y] = 1
    n = size
    while n > 0:
        if value(x+dx, y+dy) == None or value(x+dx+dx, y+dy+dy) == 1:
            dx, dy = next(diff)
            n -= 1
        else:
            x, y = x+dx, y+dy
            spiral[x][y] = 1

    return spiral


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(spiralize(5), [[1,1,1,1,1],
                             [0,0,0,0,1],
                             [1,1,1,0,1],
                             [1,0,0,0,1],
                             [1,1,1,1,1]])
assert_equals(spiralize(8), [[1,1,1,1,1,1,1,1],
                             [0,0,0,0,0,0,0,1],
                             [1,1,1,1,1,1,0,1],
                             [1,0,0,0,0,1,0,1],
                             [1,0,1,0,0,1,0,1],
                             [1,0,1,1,1,1,0,1],
                             [1,0,0,0,0,0,0,1],
                             [1,1,1,1,1,1,1,1]])
