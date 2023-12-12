# https://www.codewars.com/kata/54acd76f7207c6a2880012bb

# %%
morse = {
'A': '.-',
'B': '-...',
'C': '-.-.',
'D': '-..',
'E': '.',
'F': '..-.',
'G': '--.',
'H': '....',
'I': '..',
'J': '.---',
'K': '-.-',
'L': '.-..',
'M': '--',
'N': '-.',
'O': '---',
'P': '.--.',
'Q': '--.-',
'R': '.-.',
'S': '...',
'T': '-',
'U': '..-',
'V': '...-',
'W': '.--',
'X': '-..-',
'Y': '-.--',
'Z': '--..',
'0': '-----',
'1': '.----',
'2': '..---',
'3': '...--',
'4': '....-',
'5': '.....',
'6': '-....',
'7': '--...',
'8': '---..',
'9': '----.',
'.': '.-.-.-',
',': '--..--',
'?': '..--..',
"'": '.----.',
'!': '-.-.--',
'/': '-..-.',
'(': '-.--.',
')': '-.--.-',
'&': '.-...',
':': '---...',
';': '-.-.-.',
'=': '-...-',
'+': '.-.-.',
'-': '-....-',
'_': '..--.-',
'"': '.-..-.',
'$': '...-..-',
'@': '.--.-.',
'SOS': '...---...',
}
MORSE_CODE = {v:k for k,v in morse.items()}

import re
from sklearn.cluster import KMeans
import numpy as np

def decode_char(ch):
    return MORSE_CODE[ch]

def decode_word(word):
    return ''.join(map(decode_char, word.split(' ')))

def decodeMorse(code):
    if code == '':
        return ''
    return ' '.join(map(decode_word, code.split('   ')))

def decodeBitsAdvanced(bits):
    s = bits.strip('0')
    if s == '':
        return ''

    chunks = re.split(r'(0+|1+)', s)
    chunks = list(filter(len, chunks))
    lens = list(sorted(set(map(len, chunks))))

    if len(lens) == 2:
        v = (lens[1]-lens[0])//2
        if v > 0:
            lens.append(v)
            lens = list(sorted(set(lens)))

    labels = {
        '0': ['',' ','   '],
        '1': ['.','-'],
    }

    n_classes = min(3, len(lens))        
    X = np.array(lens).reshape(-1,1)
    clf = KMeans(n_clusters=n_classes, random_state=0).fit(X)
    clf.cluster_centers_ = np.sort(clf.cluster_centers_, axis=0)

    for _ in range(10):
        classes = dict(zip(lens, clf.predict(X)))
        code = ''.join([labels[v[0]][classes[len(v)]] for v in chunks])
        try:
            decodeMorse(code)
            return code
        except KeyError:
            clf.cluster_centers_ -= 1
    
    return ''


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(decodeMorse(decodeBitsAdvanced('0000000011011010011100000110000001111110100111110011111100000000000111011111111011111011111000000101100011111100000111110011101100000100000')), 'HEY JUDE')
assert_equals(decodeMorse(decodeBitsAdvanced('0000')), '')
assert_equals(decodeMorse(decodeBitsAdvanced('')), '')
assert_equals(decodeMorse(decodeBitsAdvanced('1001')), 'EE')
assert_equals(decodeMorse(decodeBitsAdvanced('10001')), 'EE')
assert_equals(decodeMorse(decodeBitsAdvanced('100001')), 'EE')
assert_equals(decodeMorse(decodeBitsAdvanced('10000001')), 'E E')
assert_equals(decodeMorse(decodeBitsAdvanced('100000001')), 'E E')
assert_equals(decodeMorse(decodeBitsAdvanced('1000000001')), 'E E')
assert_equals(decodeMorse(decodeBitsAdvanced('10000000001')), 'E E')
assert_equals(decodeMorse(decodeBitsAdvanced('1110111')), 'M')
assert_equals(decodeMorse(decodeBitsAdvanced('111')), 'E')
assert_equals(decodeMorse(decodeBitsAdvanced('1111111')), 'E')
assert_equals(decodeMorse(decodeBitsAdvanced('11111100111111')), 'M')
assert_equals(decodeMorse(decodeBitsAdvanced('01110')), 'E')
assert_equals(decodeMorse(decodeBitsAdvanced('000000011100000')), 'E')
assert_equals(decodeMorse(decodeBitsAdvanced('00000000000111111100000011010001110111000000001110000000000000000001111111011111100001101111100000111100111100011111100000001011100000011111110010001111100110000011111100101111100000000000000111111100001111010110000011000111110010000011111110001111110011111110000010001111110001111111100000001111111101110000000000000010110000111111110111100000111110111110011111110000000011111001011011111000000000000111011111011111011111000000010001001111100000111110111111110000001110011111100011111010000001100001001000000000000000000111111110011111011111100000010001001000011111000000100000000101111101000000000000011111100000011110100001001100000000001110000000000000001101111101111000100000100001111111110000000001111110011111100011101100000111111000011011111000111111000000000000000001111110000100110000011111101111111011111111100000001111110001111100001000000000000000000000000000000000000000000000000000000000000')), 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG')
