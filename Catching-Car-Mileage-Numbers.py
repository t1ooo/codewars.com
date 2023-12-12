# https://www.codewars.com/kata/52c4dd683bfd3b434c000292

# %%
import re

def is_interesting(number, awesome_phrases):
    def check(number):
        # A number is only interesting if it is greater than 99!
        if number <= 99: return False
        
        # The digits match one of the values in the awesome_phrases array
        if number in awesome_phrases: return True

        number_s = str(number)
        
        # The digits are a palindrome: 1221 or 73837
        if number_s == number_s[::-1]: return True
        
        # The digits are sequential, incementing: 1234
        if number_s in '1234567890': return True
        
        # The digits are sequential, decrementing: 4321
        if number_s in '9876543210': return True
        
        # Every digit is the same number: 1111
        if len(set(number_s)) == 1: return True
        
        # Any digit followed by all zeros
        if re.search(r'0{2,}$', number_s): return True
            
        return False


    if check(number):   return 2
    if check(number+1): return 1
    if check(number+2): return 1
    return 0



def assert_equals(actual, expected, msg=None):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


tests = [
    {'n': 3, 'interesting': [1337, 256], 'expected': 0},
    {'n': 1336, 'interesting': [1337, 256], 'expected': 1},
    {'n': 1337, 'interesting': [1337, 256], 'expected': 2},
    {'n': 11208, 'interesting': [1337, 256], 'expected': 0},
    {'n': 11209, 'interesting': [1337, 256], 'expected': 1},
    {'n': 11211, 'interesting': [1337, 256], 'expected': 2},
]
for t in tests:
    assert_equals(is_interesting(t['n'], t['interesting']), t['expected'], t)
