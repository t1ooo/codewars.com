# https://www.codewars.com/kata/517abf86da9663f1d2000003

# %%
import re

def to_camel_case(text):
    '''
    >>> to_camel_case("")
    ''
    >>> to_camel_case("the_stealth_warrior")
    'theStealthWarrior'
    >>> to_camel_case("The-Stealth-Warrior")
    'TheStealthWarrior'
    >>> to_camel_case("A-B-C")
    'ABC'
    '''
    return re.sub(r'[\-\_](\w)', lambda m: m.group(1).upper(), text)


import doctest
doctest.testmod()
