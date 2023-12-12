# https://www.codewars.com/kata/520b9d2ad5c005041100000f

# %%
import re

def pig_word(word):
    if re.match(r'(?i)[^a-z]', word):
        return word
    return word[1:] + word[:1] + 'ay'

def pig_it(text):
    return ' '.join([pig_word(w) for w in text.split(' ')])


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(pig_it('Pig latin is cool'), 
              'igPay atinlay siay oolcay')
assert_equals(pig_it('This is my string'), 
              'hisTay siay ymay tringsay')
assert_equals(pig_it('Quis custodiet ipsos custodes ?'),
              'uisQay ustodietcay psosiay ustodescay ?')
assert_equals(pig_it("O tempora o mores !"),
              'Oay emporatay oay oresmay !')
