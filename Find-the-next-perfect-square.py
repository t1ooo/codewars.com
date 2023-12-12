# https://www.codewars.com/kata/56269eb78ad2e4ced1000013

# %%
def find_next_square(sq):
    '''
    >>> find_next_square(121)
    144
    >>> find_next_square(625)
    676
    >>> find_next_square(319225)
    320356
    >>> find_next_square(15241383936)
    15241630849
    >>> find_next_square(155)
    -1
    >>> find_next_square(342786627)
    -1
    '''
    n = (sq**0.5)
    if n == int(n):
        return int((n+1)**2)
    return -1


import doctest
doctest.testmod()
