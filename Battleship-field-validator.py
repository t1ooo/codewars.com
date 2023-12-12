# https://www.codewars.com/kata/52bb6539a4cf1b12d90005b7

# %%
import numpy as np


def validate_battlefield(field):
    field = np.pad(field, 1)

    def count(mask):
        a, b = mask.shape
        return np.sum([(field[y:y+a, x:x+b] == mask).all()
                       for y in range(len(field)-a+1)
                       for x in range(len(field[y])-b+1)])

    for i in range(1, 5):
        mask = np.pad([[1] * i], 1)
        c = count(mask) + (count(mask.T) if i > 1 else 0)
        if c != 5 - i:
            return False

    return True


# TEST
def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


battleField = [[1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
               [1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
               [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
assert_equals(validate_battlefield(battleField),
              True, "Nope, something is wrong!")


battleField = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 1, 1, 1, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
               [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 1, 0, 1, 0, 1, 1, 0], ]
assert_equals(validate_battlefield(battleField),
              True, "Nope, something is wrong!")

