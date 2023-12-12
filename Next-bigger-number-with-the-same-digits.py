# https://www.codewars.com/kata/55983863da40caa2c900004e

# %%

def next_bigger(n):
    ds = list(str(n))[::-1]
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
            return int(''.join(new_ds)[::-1])

    return -1


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(next_bigger(12),   21)
assert_equals(next_bigger(21),   -1)
assert_equals(next_bigger(513),  531)
assert_equals(next_bigger(2017), 2071)
assert_equals(next_bigger(414),  441)
assert_equals(next_bigger(144),  414)
assert_equals(next_bigger(1234567890),  1234567908)
