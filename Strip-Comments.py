# https://www.codewars.com/kata/51c8e37cee245da6b40000bd

# %%
import re


def strip_comments_v1(string, markers):
    lines = []
    for line in string.split('\n'):
        for m in markers:
            if (i := line.find(m)) != -1:
                line = line[:i]
        lines.append(line.rstrip())
    return '\n'.join(lines)


def strip_comments_v2(string, markers):
    lines = []
    for line in string.split('\n'):
        for i, ch in enumerate(line):
            if ch in markers:
                line = line[:i]
                break
        lines.append(line.rstrip())
    return '\n'.join(lines)


def strip_comments(string, markers):
    p = fr'[ \t]*(\n|$)+'
    if len(markers) > 0:
        m = ''.join(map(re.escape, markers))
        p = fr'[ \t]*[{m}].*(\n|$)+'
    return re.sub(p, r'\g<1>', string)


# TEST
def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   "{actual}"\nexpected: "{expected}"'


assert_equals(strip_comments('apples, pears # and bananas\ngrapes\nbananas !apples', [
              '#', '!']), 'apples, pears\ngrapes\nbananas')
assert_equals(strip_comments('a #b\nc\nd $e f g', ['#', '$']), 'a\nc\nd')
assert_equals(strip_comments(' a #b\nc\nd $e f g', ['#', '$']), ' a\nc\nd')
assert_equals(strip_comments('  oranges watermelons oranges ? strawberries ?\nlemons lemons\navocados , , oranges\nstrawberries # @ oranges',
              []), '  oranges watermelons oranges ? strawberries ?\nlemons lemons\navocados , , oranges\nstrawberries # @ oranges')


assert_equals(strip_comments("\t^ ' ^ ^ avocados\npears cherries apples\n^ !\nwatermelons ' @\nlemons lemons apples @ lemons", ['!', '?', ',', '=', "'", '#', '^', '.']),
              '\npears cherries apples\n\nwatermelons\nlemons lemons apples @ lemons')
