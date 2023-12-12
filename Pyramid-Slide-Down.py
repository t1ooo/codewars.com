# https://www.codewars.com/kata/551f23362ff852e2ab000037

#%%
# Execution Timed Out (12000 ms)
def longest_slide_down_try1(pyramid):
    def dfs(s, i, k):
        if i < len(pyramid) and k < len(pyramid[i]):
            v = pyramid[i][k]
            left = v + dfs(s, i+1, k)
            right = v + dfs(s, i+1, k+1)
            return max(left, right)
        return 0

    return dfs(pyramid, 0, 0)


# Execution Timed Out (12000 ms)
def longest_slide_down_try2(pyramid):
    def dfs(s, i, k):
        if i < len(pyramid) and k < len(pyramid[i]):
            v = pyramid[i][k]
            left = v + dfs(s, i+1, k)
            right = v + dfs(s, i+1, k+1)
            return max(left, right)
        return 0

    return dfs(pyramid, 0, 0)


def longest_slide_down_v1(pyramid):
    s = [[v] for v in pyramid[-1]]
    for row in reversed(pyramid[:-1]):
        for k,v in enumerate(row):
            sk = [v+q for kk in [k,k+1] for q in s[kk]]
            sk.sort(reverse=True)
            sk = sk[:int(len(sk)/2)]
            s[k] = sk
    return max(s[0])


def longest_slide_down(pyramid):
    s = [[v] for v in pyramid[-1]]
    for row in reversed(pyramid[:-1]):
        for k,v in enumerate(row):
            s[k] = [v+max(s[k]), v+max(s[k+1])]
    return max(s[0])


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


assert_equals(longest_slide_down([
    [3],
  [7, 4],
 [2, 4, 6],
[8, 5, 9, 3]]), 23)


assert_equals(longest_slide_down([
[75],
[95, 64],
[17, 47, 82],
[18, 35, 87, 10],
[20,  4, 82, 47, 65],
[19,  1, 23, 75,  3, 34],
[88,  2, 77, 73,  7, 63, 67],
[99, 65,  4, 28,  6, 16, 70, 92],
[41, 41, 26, 56, 83, 40, 80, 70, 33],
[41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
[53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
[70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
[91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
[63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
[ 4, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23],
]), 1074)

