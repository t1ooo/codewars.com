# https://www.codewars.com/kata/5254ca2719453dcc0b00027d

# %%

def next_bigger(n):
    ds = list(n)[::-1]
    for i in range(len(ds)-1):
        if ds[i] > ds[i+1]:
            k = i+1

            swap_k = None
            for j in range(k):
                if ds[j] > ds[k]:
                    swap_k = j
                    break
            if swap_k is None:
                break

            ds[k], ds[swap_k] = ds[swap_k], ds[k]
            new_ds = sorted(ds[:k], reverse=True) + [ds[k]] + ds[k+1:]
            return ''.join(new_ds)[::-1]

    return None


def permutations_v1(s):
    s = ''.join(sorted(s))
    result = [s]
    while (s := next_bigger(s)) is not None:
        result.append(s)
    return result


def permutations(s):
    if len(s) == 1:
        return [s]
    if len(s) == 2:
        return list(set([s, s[::-1]]))
    
    head, tail = s[:len(s)-1], s[len(s)-1:]
    result = []
    for p in permutations(head):
        for i in range(len(p)+1):
            result.append(p[:i] + tail +p[i:])

    return list(set(result))


# TEST
def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(sorted(permutations('a')), ['a'])
assert_equals(sorted(permutations('ab')), ['ab', 'ba'])
assert_equals(sorted(permutations('aabb')), [
              'aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa'])



# permutations_v1('1234')
# for a in range(1,4):
#     for b in range(1,4):
#         for c in range(1,4):
#             if a == b or b == c or a == c: continue
#             print(f'{a}{b}{c}')

permutations('aa')
