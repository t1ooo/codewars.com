# https://www.codewars.com/kata/527fde8d24b9309d9b000c4e

# %%
import numpy as np

def value(lst, i, k ,default=None):
    if  0<=i<len(lst) \
    and 0<=k<len(lst[i]):
        return lst[i,k]
    return default


def remove_spaces(lines):
    del_rows = []
    for i in range(len(lines)):
        if (np.all(lines[i,:]==' ')):
            del_rows.append(i)
    lines = np.delete(lines, del_rows, axis=0)
    return lines


def replace_vertex(lines, edge='-'):
    assert edge in ('-', '|')

    patterns = [
        '-+-',
        '-++',
        '++-',
        '+++',
    ]
    vertical = '|'

    if edge == '|':
        patterns = [v.replace('-', '|') for v in patterns]
        vertical = '-'

    for i in range(len(lines)):
        for k in range(len(lines[i])-2):
            if value(lines, i-1, k+1) == vertical \
            or value(lines, i+1, k+1) == vertical:
                continue
            for pat in patterns:
                if ''.join(lines[i,k:k+3]) == pat:
                    lines[i,k+1] = edge
                    break
    
    return lines


def fmt(split, path):
    lines = []
    for i in range(len(split)):
        line = []
        for k in range(len(split[i])):
            if (i,k) in path:
                line.append(split[i,k])
            else:
                line.append(' ')
        lines.append(line)
    lines = np.array(lines)

    lines = remove_spaces(lines)
    lines = np.transpose(lines)
    lines = remove_spaces(lines)
    lines = np.transpose(lines)
    
    lines = replace_vertex(lines, '-')
    lines = np.transpose(lines)
    lines = replace_vertex(lines, '|')
    lines = np.transpose(lines)

    return '\n'.join([''.join(l).rstrip() for l in lines])


def split_shape(shape):
    splited = list(filter(len, shape.split('\n')))
    max_len = max(map(len, splited))
    return [list(v.ljust(max_len, ' ')) for v in splited]


def break_pieces(shape):
    shape_arr = np.array(split_shape(shape))

    def f(i, k, visited):
        v = value(shape_arr, i,k)
        if value == None:
            return True
        
        if (i,k) in visited:
            return True
        visited.add((i,k))

        if v == ' ':
            if 0==i or i==len(shape_arr)-1 \
            or 0==k or k==len(shape_arr[i])-1:
                return False

            for di in [-1,0,1]:
                for dk in [-1,0,1]:
                    if not f(i+di, k+dk, visited):
                        return False

        return True
    
    result = []
    all_visited = set()
    for i in range(len(shape_arr)):
        for k in range(len(shape_arr[i])):
            if shape_arr[i,k] != ' ': continue
            if (i,k) in all_visited: continue
            visited = set()
            if f(i, k, visited):
                r = fmt(shape_arr, visited)
                result.append(r)
            all_visited |= visited

    return result


def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


test_data = [
    ('Description example',
     [('\n+------------+\n|            |\n|            |\n|            |\n+------+-----+\n|      |     |\n|      |     |\n+------+-----+', ['+-----+\n|     |\n|     |\n+-----+', '+------+\n|      |\n|      |\n+------+', '+------------+\n|            |\n|            |\n|            |\n+------------+'])]),
    ('Simple shapes',
     [('\n+-------------------+--+\n|                   |  |\n|                   |  |\n|  +----------------+  |\n|  |                   |\n|  |                   |\n+--+-------------------+', ['                 +--+\n                 |  |\n                 |  |\n+----------------+  |\n|                   |\n|                   |\n+-------------------+', '+-------------------+\n|                   |\n|                   |\n|  +----------------+\n|  |\n|  |\n+--+']),
      ('\n           +-+             \n           | |             \n         +-+-+-+           \n         |     |           \n      +--+-----+--+        \n      |           |        \n   +--+-----------+--+     \n   |                 |     \n   +-----------------+     ', ['+-+\n| |\n+-+', '+-----+\n|     |\n+-----+', '+-----------+\n|           |\n+-----------+', '+-----------------+\n|                 |\n+-----------------+']),
      ('\n+---+---+---+---+---+---+---+---+\n|   |   |   |   |   |   |   |   |\n+---+---+---+---+---+---+---+---+', ['+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n+---+']),
      ('\n+---+------------+---+\n|   |            |   |\n+---+------------+---+\n|   |            |   |\n|   |            |   |\n|   |            |   |\n|   |            |   |\n+---+------------+---+\n|   |            |   |\n+---+------------+---+', ['+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n+---+', '+---+\n|   |\n|   |\n|   |\n|   |\n+---+', '+---+\n|   |\n|   |\n|   |\n|   |\n+---+', '+------------+\n|            |\n+------------+', '+------------+\n|            |\n+------------+', '+------------+\n|            |\n|            |\n|            |\n|            |\n+------------+']),
      ('\n                 \n   +-----+       \n   |     |       \n   |     |       \n   +-----+-----+ \n         |     | \n         |     | \n         +-----+ ', ['+-----+\n|     |\n|     |\n+-----+', '+-----+\n|     |\n|     |\n+-----+'])]),
    ('Nested pieces',
     [('\n+--------+\n|        |\n|  +--+  |\n|  |  |  |\n|  +--+  |\n|        |\n+--------+', ['+--+\n|  |\n+--+', '+--------+\n|        |\n|  +--+  |\n|  |  |  |\n|  +--+  |\n|        |\n+--------+'])]),
    ('Convoluted borders',
     [('\n+-------+ +----------+\n|       | |          |\n| +-+ +-+ +-+    +-+ |\n+-+ | |     |  +-+ +-+\n    | +-----+--+\n+-+ |          +-+ +-+\n| +-+  +----+    | | |\n| |    |    |    +-+ |\n| +----++ +-+        |\n|       | |          |\n+-------+ +----------+', ['+-+\n| |\n| |\n| +-----+\n|       |\n+-------+', '+-------+\n|       |\n| +-+ +-+\n+-+ | |\n    | +--------+\n    |          +-+ +-+\n  +-+  +----+    | | |\n  |    |    |    +-+ |\n  +----+  +-+        |\n          |          |\n          +----------+', '+----------+\n|          |\n+-+    +-+ |\n  |  +-+ +-+\n  +--+'])]),
    ('edo_red97\'s big shape',
     [('\n         +------------+--+      +--+\n         |            |  |      |  |\n         | +-------+  |  |      |  |\n         | |       |  |  +------+  |\n         | |       |  |            |\n         | |       |  |    +-------+\n         | +-------+  |    |        \n +-------+            |    |        \n |       |            |    +-------+\n |       |            |            |\n +-------+            |            |\n         |            |            |\n    +----+---+--+-----+------------+\n    |    |   |  |     |            |\n    |    |   |  +-----+------------+\n    |    |   |                     |\n    +----+---+---------------------+\n    |    |                         |\n    |    | +----+                  |\n+---+    | |    |     +------------+\n|        | |    |     |             \n+--------+-+    +-----+             ', ['    +----+\n    |    |\n    |    |\n+---+    |\n|        |\n+--------+', '+--+\n|  |\n|  +------------------+\n|                     |\n+---------------------+', '+--+      +--+\n|  |      |  |\n|  |      |  |\n|  +------+  |\n|            |\n|    +-------+\n|    |\n|    |\n|    +-------+\n|            |\n|            |\n|            |\n+------------+', '+---+\n|   |\n|   |\n|   |\n+---+', '+----+\n|    |\n|    |\n|    |\n+----+', '+-----+\n|     |\n+-----+', '+-------+\n|       |\n|       |\n+-------+', '+-------+\n|       |\n|       |\n|       |\n+-------+', '+------------+\n|            |\n+------------+', '+------------+\n|            |\n| +-------+  |\n| |       |  |\n| |       |  |\n| |       |  |\n| +-------+  |\n|            |\n|            |\n|            |\n|            |\n|            |\n+------------+', '+-------------------------+\n|                         |\n| +----+                  |\n| |    |     +------------+\n| |    |     |\n+-+    +-----+'])])]


for name, test_cases in test_data:
    print(name)
    for shape, expected in test_cases:
        actual = break_pieces(shape)
        message = [f'\n{name} : break_pieces failed on this shape:', shape, '', 'Actual result:']
        message.extend(actual)
        message.append('\nExpected result:')
        message.extend(expected)
        message = '\n'.join(message)
        assert_equals(sorted(actual), expected, message)
