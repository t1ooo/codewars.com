# https://www.codewars.com/kata/5265b0885fda8eac5900093b

# %%
import enum
import operator
import string
from attr import dataclass


class TokenType(enum.Enum):
    L_BRACKET = enum.auto()  # [
    R_BRACKET = enum.auto()  # ]
    L_PAREN = enum.auto()   # (
    R_PAREN = enum.auto()   # )
    PLUS = enum.auto()      # +
    MINUS = enum.auto()     # -
    STAR = enum.auto()      # *
    SLASH = enum.auto()     # /
    NUMBER = enum.auto()    # 123
    VARIABLE = enum.auto()  # abc


@dataclass
class Token:
    text: str
    type: TokenType


def scan(source: str) -> list[Token]:
    tokens = []
    i = 0

    def append_token(text, type):
        tokens.append(Token(text, type))

    def scan_token(chars, type):
        nonlocal i
        start = i
        while i < len(source) and source[i] in chars:
            i += 1
        append_token(source[start:i], type)
        i -= 1

    while i < len(source):
        ch = source[i]
        if ch == ' ':
            pass
        elif ch == '[':
            append_token(ch, TokenType.L_BRACKET)
        elif ch == ']':
            append_token(ch, TokenType.R_BRACKET)
        elif ch == '(':
            append_token(ch, TokenType.L_PAREN)
        elif ch == ')':
            append_token(ch, TokenType.R_PAREN)
        elif ch == '+':
            append_token(ch, TokenType.PLUS)
        elif ch == '-':
            append_token(ch, TokenType.MINUS)
        elif ch == '*':
            append_token(ch, TokenType.STAR)
        elif ch == '/':
            append_token(ch, TokenType.SLASH)
        elif ch in string.digits:
            scan_token(string.digits, TokenType.NUMBER)
        elif ch in string.ascii_lowercase:
            scan_token(string.ascii_lowercase, TokenType.VARIABLE)
        else:
            raise Exception(f'undefined token:{ch}')

        i += 1

    return tokens


class Expr:
    def to_dict(self) -> dict:
        raise NotImplementedError()


@dataclass
class Unary(Expr):
    op: str
    n: int

    def to_dict(self) -> dict:
        return {
            'op': self.op,
            'n': self.n,
        }


@dataclass
class Binary(Expr):
    op: str
    a: Expr
    b: Expr

    def to_dict(self) -> dict:
        return {
            'op': self.op,
            'a': self.a.to_dict(),
            'b': self.b.to_dict(),
        }


def parse(tokens: list[Token]) -> Expr:
    i = 0
    args = []

    def has_next():
        return i < len(tokens)

    def match(token, *types):
        return token.type in types

    def factor() -> Expr:
        nonlocal i

        if match(tokens[i], TokenType.NUMBER):
            n = int(tokens[i].text)
            expr = Unary('imm', n)
            i += 1
            return expr

        if match(tokens[i], TokenType.VARIABLE):
            name = tokens[i].text
            nonlocal args
            n = args.index(name)
            expr = Unary('arg', n)
            i += 1
            return expr

        if match(tokens[i], TokenType.L_PAREN):
            i += 1
            expr = expression()
            if not (has_next() and match(tokens[i], TokenType.R_PAREN)):
                raise Exception('expect ")"')
            i += 1
            return expr

        raise Exception(f'invalid input')

    def binary() -> Expr:
        nonlocal i
        expr = factor()
        while has_next() and match(tokens[i], TokenType.STAR, TokenType.SLASH):
            op = tokens[i]
            i += 1
            right = factor()
            expr = Binary(op.text, expr, right)
        return expr

    def expression() -> Expr:
        nonlocal i
        expr = binary()
        while has_next() and match(tokens[i], TokenType.PLUS, TokenType.MINUS):
            op = tokens[i]
            i += 1
            right = binary()
            expr = Binary(op.text, expr, right)
        return expr

    def function() -> Expr:
        nonlocal i
        i += 1
        params = []
        while has_next() and match(tokens[i], TokenType.VARIABLE):
            params.append(tokens[i].text)
            i += 1
        if not (has_next() and match(tokens[i], TokenType.R_BRACKET)):
            raise Exception('expect "]"')
        i += 1

        nonlocal args
        args = params.copy()
        body = expression()
        args.clear()

        return body

    if match(tokens[i], TokenType.L_BRACKET):
        return function()
    else:
        return expression()


def reduce(ast: dict) -> dict:
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
    }

    op = ast['op']
    if op in '+-*/':
        a, b = reduce(ast['a']), reduce(ast['b'])
        if a['op'] == 'imm' and b['op'] == 'imm':
            return {
                'n': ops[op](a['n'], b['n']),
                'op': 'imm'
            }
        return {'op': op, 'a': a, 'b': b}

    return ast


def assembly(ast: dict) -> list:
    ops = {
        '+': 'AD',
        '-': 'SU',
        '*': 'MU',
        '/': 'DI',
    }

    op = ast['op']
    if op in '+-*/':
        a, b = assembly(ast['a']), assembly(ast['b'])
        return a + ['PU'] + b + ['SW', 'PO', ops[op]]
    elif op == 'arg':
        return [f'AR {ast["n"]}']
    elif op == 'imm':
        return [f'IM {ast["n"]}']
    else:
        raise Exception(f'undefined op: {op}')


class Compiler(object):
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = scan(program)
        expr = parse(tokens)
        return expr.to_dict()

    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        return reduce(ast)

    def pass3(self, ast):
        """Returns assembly instructions"""
        return assembly(ast)


# TEST

def assert_equals(actual, expected, msg=''):
    assert actual == expected, f'{msg}\nactual:   {actual}\nexpected: {expected}'


def simulate(asm, argv):
    r0, r1 = None, None
    stack = []
    n, r0, r1 = 0, 0, 0
    for ins in asm:
        if ins[:2] == 'IM' or ins[:2] == 'AR':
            ins, n = ins[:2], int(ins[2:])
        if ins == 'IM':
            r0 = n
        elif ins == 'AR':
            r0 = argv[n]
        elif ins == 'SW':
            r0, r1 = r1, r0
        elif ins == 'PU':
            stack.append(r0)
        elif ins == 'PO':
            r0 = stack.pop()
        elif ins == 'AD':
            r0 += r1
        elif ins == 'SU':
            r0 -= r1
        elif ins == 'MU':
            r0 *= r1
        elif ins == 'DI':
            r0 /= r1
    return r0


def example_tests():
    prog = '[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)'
    t1 = {'op': '/', 'a': {'op': '-', 'a': {'op': '+', 'a': {'op': '*', 'a': {'op': '*', 'a': {'op': 'imm', 'n': 2}, 'b': {'op': 'imm', 'n': 3}}, 'b': {'op': 'arg', 'n': 0}}, 'b': {'op': '*', 'a': {'op': 'imm', 'n': 5}, 'b': {'op': 'arg', 'n': 1}}},
                           'b': {'op': '*', 'a': {'op': 'imm', 'n': 3}, 'b': {'op': 'arg', 'n': 2}}}, 'b': {'op': '+', 'a': {'op': '+', 'a': {'op': 'imm', 'n': 1}, 'b': {'op': 'imm', 'n': 3}}, 'b': {'op': '*', 'a': {'op': 'imm', 'n': 2}, 'b': {'op': 'imm', 'n': 2}}}}
    t2 = {'op': '/', 'a': {'op': '-', 'a': {'op': '+', 'a': {'op': '*', 'a': {'op': 'imm', 'n': 6}, 'b': {'op': 'arg', 'n': 0}}, 'b': {'op': '*',
                                                                                                                                       'a': {'op': 'imm', 'n': 5}, 'b': {'op': 'arg', 'n': 1}}}, 'b': {'op': '*', 'a': {'op': 'imm', 'n': 3}, 'b': {'op': 'arg', 'n': 2}}}, 'b': {'op': 'imm', 'n': 8}}

    c = Compiler()

    p1 = c.pass1(prog)
    assert_equals(p1, t1, 'Pass1')

    p2 = c.pass2(p1)
    assert_equals(p2, t2, 'Pass2')

    p3 = c.pass3(p2)
    assert_equals(simulate(p3, [4, 0, 0]), 3, 'prog(4,0,0) == 3')
    assert_equals(simulate(p3, [4, 8, 0]), 8, 'prog(4,8,0) == 8')
    assert_equals(simulate(p3, [4, 8, 16]), 2, 'prog(4,8,6) == 2')

    order_of_ops_prog = '[ x y z ] x - y - z + 10 / 5 / 2 - 7 / 1 / 7'
    order_of_ops = c.pass3(c.pass2(c.pass1(order_of_ops_prog)))
    assert_equals(
        simulate(order_of_ops, [5, 4, 1]), 0, order_of_ops_prog + ' @ [5,4,1]')


example_tests()
