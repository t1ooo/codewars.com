# https://www.codewars.com/kata/541c8630095125aba6000c00

# %%
def digital_root(n):
    '''
    >>> digital_root(16)
    7
    >>> digital_root(942)
    6
    >>> digital_root(132189)
    6
    >>> digital_root(493193)
    2
    >>> digital_root(10)
    1
    '''
    if n < 10:
        return n
    return digital_root(sum(map(int, str(n))))


import doctest
doctest.testmod()
