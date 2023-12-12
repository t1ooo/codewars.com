# https://www.codewars.com/kata/56541980fa08ab47a0000040

# %%

def printer_error(s):
    e = sum(not ('a' <= ch <= 'm') for ch in s)
    n = len(s)
    return f'{e}/{n}'


def assert_equals(a, b, msg=None):
    assert a == b, (a, b, msg) if msg else (a, b)

s = "aaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbmmmmmmmmmmmmmmmmmmmxyz"
assert_equals(printer_error(s), "3/56")
s = "kkkwwwaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbmmmmmmmmmmmmmmmmmmmxyz"
assert_equals(printer_error(s), "6/60")
s = "kkkwwwaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbmmmmmmmmmmmmmmmmmmmxyzuuuuu"
assert_equals(printer_error(s) , "11/65")
