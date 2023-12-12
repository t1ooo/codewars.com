# https://www.codewars.com/kata/57cebe1dc6fdc20c57000ac9

# %%
def find_short(s):
    return min(map(len, s.split(' ')))


def assert_equals(a, b, msg=None):
    assert a == b, (a, b, msg) if msg else (a, b)


assert_equals(find_short("bitcoin take over the world maybe who knows perhaps"), 3)
assert_equals(find_short("turns out random test cases are easier than writing out basic ones"), 3)
assert_equals(find_short("lets talk about javascript the best language"), 3)
assert_equals(find_short("i want to travel the world writing code one day"), 1)
assert_equals(find_short("Lets all go on holiday somewhere very cold"), 2)   
assert_equals(find_short("Let's travel abroad shall we"), 2)
