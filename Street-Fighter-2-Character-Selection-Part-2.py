# https://www.codewars.com/kata/58583922c1d5b415b00000ff

# %%

def do_move(fighters, position, move):
    y, x = position
    match move:
        case 'up':
            if not (y-1 < 0 or fighters[y-1][x] == ''):
                y -= 1
        case 'down':
            if not (y+1 >= len(fighters) or fighters[y+1][x] == ''):
                y += 1
        case 'left':
            x = (x-1) % len(fighters[y])
            while fighters[y][x] == '':
                y, x = do_move(fighters, (y, x), move)
        case 'right':
            x = (x+1) % len(fighters[y])
            while fighters[y][x] == '':
                y, x = do_move(fighters, (y, x), move)
        case _: raise Exception(f'undefined move: {move}')
    return (y, x)


def super_street_fighter_selection_v1(fighters, position, moves):
    y, x = position
    selections = []
    for move in moves:
        y, x = do_move(fighters, (y, x), move)
        selections.append(fighters[y][x])
    return selections


diff = {
    'up': (-1, 0),
    'down': (+1, 0),
    'right': (0, +1),
    'left': (0, -1),
}


def super_street_fighter_selection(fighters, position, moves):
    y, x = position
    selections = []
    for move in moves:
        dy, dx = diff[move]

        y = y+dy
        if not (0 <= y < len(fighters)) or fighters[y][x] == '':
            y = y-dy

        x = (x+dx) % len(fighters[y])
        while fighters[y][x] == '':
            x = (x+dx) % len(fighters[y])

        selections.append(fighters[y][x])

    return selections


# TEST
def assert_equals(actual, expected, msg='', moves=[]):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


opts = ['up', 'down', 'right', 'left']

# DO NOT CHANGE THIS VARIABLE!
fighters = [
    ['',    'Ryu',  'E.Honda',  'Blanka',   'Guile', ''],
    ['Balrog',    'Ken',  'Chun Li', 'Zangief', 'Dhalsim', 'Sagat'],
    ['Vega', 'T.Hawk', 'Fei Long',  'Deejay',   'Cammy', 'M.Bison'],
]


def copy(x):
    return [r[:] for r in x]


moves = []
position = (0, 0)
solution = []
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


moves = ['up']
position = (1, 0)
solution = ['Balrog']
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


moves = ['up']*4
position = (1, 0)
solution = ['Balrog']*4
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


moves = ['down']*4
position = (1, 0)
solution = ['Vega']*4
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


moves = ['up']*4
position = (1, 5)
solution = ['Sagat']*4
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


moves = ['down']*4
position = (1, 5)
solution = ['M.Bison']*4
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


moves = ['left']*8
position = (1, 3)
solution = ['Chun Li', 'Ken', 'Balrog', 'Sagat',
            'Dhalsim', 'Zangief', 'Chun Li', 'Ken']
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


moves = ['right']*8
position = (0, 2)
solution = ['Blanka', 'Guile', 'Ryu', 'E.Honda',
            'Blanka', 'Guile', 'Ryu', 'E.Honda']
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


moves = ['right']*6+['down']+['left']*12+['down']+['right']*12
position = (0, 2)
solution = ['Blanka', 'Guile', 'Ryu', 'E.Honda', 'Blanka', 'Guile', 'Dhalsim', 'Zangief', 'Chun Li', 'Ken', 'Balrog', 'Sagat', 'Dhalsim', 'Zangief', 'Chun Li', 'Ken',
            'Balrog', 'Sagat', 'Dhalsim', 'Cammy', 'M.Bison', 'Vega', 'T.Hawk', 'Fei Long', 'Deejay', 'Cammy', 'M.Bison', 'Vega', 'T.Hawk', 'Fei Long', 'Deejay', 'Cammy']
assert_equals(super_street_fighter_selection(
    copy(fighters), position, moves), solution)


# DO NOT CHANGE THIS VARIABLE!
# LIST WITH HOLES AND DUPLICATES
fighters3 = [
    ['',    'Ryu',  'E.Honda',  'Cammy',  'Blanka',   'Guile',        '', 'Chun Li'],
    ['Balrog',    'Ken',  'Chun Li',       '',
        'M.Bison', 'Zangief', 'Dhalsim', 'Sagat'],
    ['Vega',       '', 'Fei Long', 'Balrog',
        'Deejay',   'Cammy',        '', 'T.Hawk']
]


moves = ['right']*6+['down']+['left']*12+['down']+['right']*12
position = (0, 2)
solution = ['Cammy', 'Blanka', 'Guile', 'Chun Li', 'Ryu', 'E.Honda', 'Chun Li', 'Ken', 'Balrog', 'Sagat', 'Dhalsim', 'Zangief', 'M.Bison', 'Chun Li', 'Ken', 'Balrog',
            'Sagat', 'Dhalsim', 'Zangief', 'Cammy', 'T.Hawk', 'Vega', 'Fei Long', 'Balrog', 'Deejay', 'Cammy', 'T.Hawk', 'Vega', 'Fei Long', 'Balrog', 'Deejay', 'Cammy']
assert_equals(super_street_fighter_selection(
    copy(fighters3), position, moves), solution)


moves = ['down']+['right']*3+['down']+['left']*2+['down']+['right']*3+['up']
position = (0, 3)
solution = ['Cammy', 'Blanka', 'Guile', 'Chun Li', 'Sagat', 'Dhalsim',
            'Zangief', 'Cammy', 'T.Hawk', 'Vega', 'Fei Long', 'Chun Li']
assert_equals(super_street_fighter_selection(
    copy(fighters3), position, moves), solution)

fighters4 = [
    ['',     'Ryu',  'E.Honda',  'Cammy'],
    ['Balrog',     'Ken',  'Chun Li',       ''],
    ['Vega',        '', 'Fei Long', 'Balrog', ],
    ['Blanka',   'Guile',         '', 'Chun Li'],
    ['M.Bison', 'Zangief',  'Dhalsim', 'Sagat'],
    ['Deejay',   'Cammy',         '', 'T.Hawk']
]


moves = ['left']*2+['down']+['right']*4+['down']+['left']*4+['down'] + \
    ['right']*2+['down']+['right']*3+['down']+['left']*3+['down']+['left']*3
position = (0, 3)
solution = ['E.Honda', 'Ryu', 'Ken', 'Chun Li', 'Balrog', 'Ken', 'Chun Li', 'Fei Long', 'Vega', 'Balrog', 'Fei Long', 'Vega', 'Blanka',
            'Guile', 'Chun Li', 'Sagat', 'M.Bison', 'Zangief', 'Dhalsim', 'Dhalsim', 'Zangief', 'M.Bison', 'Sagat', 'T.Hawk', 'Cammy', 'Deejay', 'T.Hawk']
assert_equals(super_street_fighter_selection(
    copy(fighters4), position, moves), solution)


moves = ['left']*2+['down']+['right']*4+['down'] + \
    ['left']*4+['up']+['right']*2+['up']+['right']*3
position = (3, 3)
solution = ['Guile', 'Blanka', 'M.Bison', 'Zangief', 'Dhalsim', 'Sagat', 'M.Bison', 'Deejay', 'T.Hawk',
            'Cammy', 'Deejay', 'T.Hawk', 'Sagat', 'M.Bison', 'Zangief', 'Guile', 'Chun Li', 'Blanka', 'Guile']
assert_equals(super_street_fighter_selection(
    copy(fighters4), position, moves), solution)


fighters, position, moves = [
    ['M.Bison', 'Zangief', 'Dhalsim', 'Sagat'],
    ['', 'Ryu', 'E.Honda', 'Cammy'],
    ['Balrog', 'Ken', 'Chun Li', ''],
    ['Vega', '', 'Fei Long', 'Balrog'],
    ['Blanka', 'Guile', '', 'Chun Li'],
    ['Deejay', 'Cammy', '', 'T.Hawk']], (2, 0), ['right', 'down', 'down', 'up', 'down', 'left', 'right', 'right', 'up', 'right', 'left', 'right', 'right', 'right', 'up', 'left', 'left', 'up', 'up', 'up', 'up', 'up', 'left', 'up', 'right', 'down', 'up', 'left', 'right', 'up', 'right', 'left', 'right', 'right', 'down', 'left', 'right']
solution = ['Ken', 'Ken', 'Ken', 'Ryu', 'Ken', 'Balrog', 'Ken', 'Chun Li', 'E.Honda', 'Cammy', 'E.Honda', 'Cammy', 'Ryu', 'E.Honda', 'Dhalsim', 'Zangief', 'M.Bison', 'M.Bison', 'M.Bison',
            'M.Bison', 'M.Bison', 'M.Bison', 'Sagat', 'Sagat', 'M.Bison', 'M.Bison', 'M.Bison', 'Sagat', 'M.Bison', 'M.Bison', 'Zangief', 'M.Bison', 'Zangief', 'Dhalsim', 'E.Honda', 'Ryu', 'E.Honda']
assert_equals(super_street_fighter_selection(
    fighters, position, moves), solution, '', moves)
