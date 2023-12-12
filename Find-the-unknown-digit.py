# https://www.codewars.com/kata/546d15cebed2e10334000ed9

# %%
import re


def solve_runes_v1(runes):
    expr = runes.replace('=', '==')
    for n in range(10):
        if str(n) in expr: continue
        if n == 0 and '??' in expr: continue
        e = expr.replace('?', str(n))
        try:
            if eval(e): return n
        except: pass
    return -1


def solve_runes(runes):
    for n in '0123456789':
        expr = runes.replace('=', '==').replace('?', n)
        if n in runes: continue
        if re.findall(r'(^|[^\d])0\d', expr): continue
        if eval(expr): return int(n)
    return -1


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(solve_runes("-?56373--9216=-?47157"), 8, "Answer for expression '-?56373--9216=-?47157' ");
assert_equals(solve_runes("123?45*?=?"), 0, "Answer for expression '123?45*?=?' ");
assert_equals(solve_runes("?38???+595???=833444"), 2, "Answer for expression '?38???+595???=833444' ");
assert_equals(solve_runes("-5?*-1=5?"), 0, "Answer for expression '1+1=?' ");
assert_equals(solve_runes("1+1=?"), 2, "Answer for expression '1+1=?' ");
assert_equals(solve_runes("123*45?=5?088"), 6, "Answer for expression '123*45?=5?088' ");
assert_equals(solve_runes("-5?*-1=5?"), 0, "Answer for expression '-5?*-1=5?' ");
assert_equals(solve_runes("19--45=5?"), -1, "Answer for expression '19--45=5?' ");
assert_equals(solve_runes("??*??=302?"), 5, "Answer for expression '??*??=302?' ");
assert_equals(solve_runes("?*11=??"), 2, "Answer for expression '?*11=??' ");
assert_equals(solve_runes("??*1=??"), 2, "Answer for expression '??*1=??' ");
