# https://www.codewars.com/kata/5502c9e7b3216ec63c0001aa

# %%
def open_or_senior(data):
    '''
    >>> open_or_senior([(45, 12),(55,21),(19, -2),(104, 20)])
    ['Open', 'Senior', 'Open', 'Senior']
    >>> open_or_senior([(16, 23),(73,1),(56, 20),(1, -1)])
    ['Open', 'Open', 'Senior', 'Open']
    '''
    def get_category(age, handicap):
        if 55 <= age and 7 < handicap:
            return 'Senior'
        return 'Open'
    
    return [get_category(*pair) for pair in data]


import doctest
doctest.testmod()
