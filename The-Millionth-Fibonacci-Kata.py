# url

# %%
from functools import cache

@cache
def _fib(n):
    if n == 0: return (0, 1)
    a, b = _fib(n // 2)
    c = a * (2*b - a)
    d = a**2 + b**2
    if n % 2 == 0: return (c, d)
    else:          return (d, c + d)


def fib(n):
    if n < 0: return (-1)**(-n+1) * fib(-n)
    return _fib(n)[0]


# TEST
def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


for n, result in [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5)]:
    assert_equals(fib(n), result, f'fib({n})')


assert_equals(fib(-1), 1)
assert_equals(fib(-6), -8)
assert_equals(fib(-96), -51680708854858323072)
assert_equals(
    fib(-500),
    -139423224561697880139724382870407283950070256587697307264108962948325571622863290691557658876222521294125
)
assert_equals(
    fib(1000),
    43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875
)

