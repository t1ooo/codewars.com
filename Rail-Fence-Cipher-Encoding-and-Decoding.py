# https://www.codewars.com/kata/58c5577d61aefcf3ff000081

# %%
import numpy as np


def encode_rail_fence_cipher_v1(s, n):
    if s == '':
        return ''
    chunks = [s[i:i+n]for i in range(0, len(s), n-1)]
    arrays = []
    for i, chunk in enumerate(chunks):
        pad_size = n - len(chunk)
        chunk = chunk + ('_'*pad_size)
        a = np.zeros((n, n), str)
        np.fill_diagonal(a, list(chunk))
        if i % 2 == 1:
            a = np.flip(a, axis=0)
        arrays.append(a)

    head, tail = arrays[0], arrays[1:]
    b = np.concatenate([head] + [a[:, 1:] for a in tail], axis=1)
    r = ''.join(''.join(v) for v in b)
    r = r.replace('_', '')

    return r


def gen_coords(s, n):
    coords = []
    x, y = 0, 0
    dy = 1
    for _ in s:
        coords.append((y, x))
        if not (0 <= (y + dy) < n):
            dy = -dy
        y += dy
        x += 1
    return coords


def fill_matrix(s, n, coords):
    m = np.zeros((n, len(s)), str)
    for (y, x), ch in zip(coords, s):
        m[y, x] = ch
    return m


def encode_rail_fence_cipher(s, n):
    coords = gen_coords(s, n)
    m = fill_matrix(s, n, coords)
    r = ''.join(''.join(v) for v in m)
    return r


def decode_rail_fence_cipher(s, n):
    coords = gen_coords(s, n)
    coords.sort()
    m = fill_matrix(s, n, coords)
    coords.sort(key=lambda x: (x[1], x[0]))
    return ''.join(m[yx] for yx in coords)


# TEST
def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(encode_rail_fence_cipher(
    "WEAREDISCOVEREDFLEEATONCE", 3), "WECRLTEERDSOEEFEAOCAIVDEN")
assert_equals(encode_rail_fence_cipher("Hello, World!", 3), "Hoo!el,Wrdl l")
assert_equals(encode_rail_fence_cipher("Hello, World!", 4), "H !e,Wdloollr")
assert_equals(encode_rail_fence_cipher("", 3), "")


assert_equals(decode_rail_fence_cipher("H !e,Wdloollr", 4), "Hello, World!")
assert_equals(decode_rail_fence_cipher(
    "WECRLTEERDSOEEFEAOCAIVDEN", 3), "WEAREDISCOVEREDFLEEATONCE")
assert_equals(decode_rail_fence_cipher("", 3), "")
