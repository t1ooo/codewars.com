# https://www.codewars.com/kata/55f8a9c06c018a0d6e000132

# %%
import re

def validate_pin(pin):
    """
    >>> validate_pin("1")
    False
    >>> validate_pin("12")
    False
    >>> validate_pin("123")
    False
    >>> validate_pin("12345")
    False
    >>> validate_pin("1234567")
    False
    >>> validate_pin("-1234")
    False
    >>> validate_pin("-12345")
    False
    >>> validate_pin("1.234")
    False
    >>> validate_pin("00000000")
    False
    >>> validate_pin("a234")
    False
    >>> validate_pin(".234")
    False
    >>> validate_pin("'1234")
    False
    >>> validate_pin("1234")
    True
    >>> validate_pin("0000")
    True
    >>> validate_pin("1111")
    True
    >>> validate_pin("123456")
    True
    >>> validate_pin("098765")
    True
    >>> validate_pin("000000")
    True
    >>> validate_pin("123456")
    True
    >>> validate_pin("090909")
    True
    """
    return bool(re.fullmatch(r'(\d{4}|\d{6})', pin))


import doctest
doctest.testmod()
