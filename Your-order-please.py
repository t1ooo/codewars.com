# https://www.codewars.com/kata/55c45be3b2079eccff00010f

# %%
def extract_position(word):
    for ch in word:
        if ch.isdigit():
            return int(ch)
    raise Exception(f'position not found: {word}')


def order(sentence):
    if sentence == '':
        return ''
    words = sentence.split(' ')
    positions = [extract_position(w) for w in words]
    sorted_words = [w for _,w in sorted(zip(positions, words))]
    return ' '.join(sorted_words)


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(order("is2 Thi1s T4est 3a"), "Thi1s is2 3a T4est")
assert_equals(order("4of Fo1r pe6ople g3ood th5e the2"), "Fo1r the2 g3ood 4of th5e pe6ople")
assert_equals(order(""), "")
