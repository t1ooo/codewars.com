# https://www.codewars.com/kata/52ffcfa4aff455b3c2000750


# %%
from enum import Enum, IntEnum
import enum
import operator
from typing import Callable


class TokenType(Enum):
    PLUS = enum.auto()
    MINUS = enum.auto()
    STAR = enum.auto()
    SLASH = enum.auto()
    PERCENT = enum.auto()

    EQUAL = enum.auto()

    FN = enum.auto()
    FN_KW = enum.auto()

    LEFT_PAREN = enum.auto()
    RIGHT_PAREN = enum.auto()

    NUMBER = enum.auto()
    IDENTIFIER = enum.auto()

    EOL = enum.auto()


class Token:
    def __init__(self, type: TokenType, lexeme: str = '') -> None:
        self.type = type
        self.lexeme = lexeme

    def __repr__(self) -> str:
        return f'({self.__class__.__name__} {self.type} {self.lexeme})'


class Scanner:
    def __init__(self):
        self.source = ''
        self.current = 0
        self.start = 0

    def scan(self, source: str) -> list[Token]:
        self.source = source
        self.current = 0
        self.start = 0

        tokens = []
        while self.current < len(self.source):
            self.start = self.current
            c = self.advance()
            if c == ' ': continue
            elif c  == '+': tokens.append(Token(TokenType.PLUS))
            elif c  == '-': tokens.append(Token(TokenType.MINUS))
            elif c  == '*': tokens.append(Token(TokenType.STAR))
            elif c  == '/': tokens.append(Token(TokenType.SLASH))
            elif c  == '%': tokens.append(Token(TokenType.PERCENT))
            elif c  == '(': tokens.append(Token(TokenType.LEFT_PAREN))
            elif c  == ')': tokens.append(Token(TokenType.RIGHT_PAREN))
            elif c  == '=': tokens.append(self.equal())
            elif self.is_digit(c): tokens.append(self.number())
            elif self.is_alpha(c): tokens.append(self.identifier())
            else: raise Exception(f'Undefined token: {c}')

        tokens.append(Token(TokenType.EOL))
        return tokens

    def advance(self) -> str:
        i = self.current
        self.current += 1
        return self.source[i]

    def peek(self, distance: int = 0) -> str:
        i = self.current + distance
        if 0 <= i < len(self.source):
            return self.source[i]
        return '\0'

    def equal(self) -> Token:
        if self.peek() == '>':
            self.advance()
            return Token(TokenType.FN)
        else:
            return Token(TokenType.EQUAL)

    def is_digit(self, c: str):
        return '0' <= c <= '9'

    def number(self) -> Token:
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek(1)):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        lexeme = self.source[self.start:self.current]
        return Token(TokenType.NUMBER, lexeme)

    def is_alpha(self, c: str):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def identifier(self) -> Token:
        while self.is_alpha(self.peek()) \
           or self.is_digit(self.peek()):
            self.advance()

        lexeme = self.source[self.start:self.current]
        type = TokenType.FN_KW if lexeme == 'fn' else TokenType.IDENTIFIER
        return Token(type, lexeme)


class Op(Enum):
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()
    NEG = enum.auto()

    SET = enum.auto()
    SET_PARAM = enum.auto()
    GET = enum.auto()

    FN = enum.auto()
    FN_RET = enum.auto()
    CALL = enum.auto()

    NUMBER = enum.auto()
    VARIABLE  = enum.auto()


class Precedence(IntEnum):
    NONE = enum.auto()
    ASSIGNMENT = enum.auto()
    TERM = enum.auto()
    FACTOR = enum.auto()
    UNARY = enum.auto()
    CALL = enum.auto()
    PRIMARY = enum.auto()


class ParseRule:
    def __init__(self,
                 prefix: Callable|None,
                 infix: Callable|None,
                 precedence: Precedence):
        self.prefix = prefix
        self.infix = infix
        self.precedence = precedence


Value = Op|int|float


class Compiler:
    def __init__(self):
        self.source = []
        self.current = 0
        self.ops = []
        self.fns = {}
        self.vars = set()
        self.rules = {
            TokenType.PLUS:ParseRule(None, self.binary, Precedence.TERM),
            TokenType.MINUS:ParseRule(self.unary, self.binary, Precedence.TERM),

            TokenType.STAR:ParseRule(None, self.binary, Precedence.FACTOR),
            TokenType.SLASH:ParseRule(None, self.binary, Precedence.FACTOR),
            TokenType.PERCENT:ParseRule(None, self.binary, Precedence.FACTOR),

            TokenType.EQUAL:ParseRule(None, self.binary, Precedence.ASSIGNMENT),

            TokenType.NUMBER:ParseRule(self.number, None, Precedence.NONE),
            TokenType.IDENTIFIER:ParseRule(self.identifier, None, Precedence.NONE),

            TokenType.LEFT_PAREN:ParseRule(self.grouping, None, Precedence.NONE),
            TokenType.RIGHT_PAREN:ParseRule(None, None, Precedence.NONE),

            TokenType.FN_KW:ParseRule(self.function, None, Precedence.NONE),
            TokenType.FN:ParseRule(None, None,  Precedence.NONE),

            TokenType.EOL: ParseRule(None, None, Precedence.NONE),
        }

    def compile(self, tokens: list[Token]) -> list[Value]:
        self.source = tokens
        self.current = 0
        self.ops = []

        if self.match(TokenType.EOL):
            return []
        self.expression()
        self.consume(TokenType.EOL, 'Expect end of expression.')
        return self.ops

    def expression(self):
        self.parse_precedence(Precedence.ASSIGNMENT)

    def parse_precedence(self, precedence: Precedence):
        self.advance()
        token = self.peek(-1)
        rule = self.rules[token.type]
        if rule.prefix is None:
            raise Exception(f'prefix is not set: {token}')
        rule.prefix()

        while precedence <= self.rules[self.peek().type].precedence:
            self.advance()
            token = self.peek(-1)
            rule = self.rules[token.type]
            if rule.infix is None:
                raise Exception(f'infix is not set: {token}')
            rule.infix()

    def function_params(self) -> list[str]:
        params = []
        while self.match(TokenType.IDENTIFIER):
            param = self.peek().lexeme
            if param in params:
                raise Exception(f'Duplicate function parameters names: {param}')
            params.append(param)
            self.advance()
        return params

    def function_body(self, params: list[str]):
        for param in params:
            self.ops.append(Op.VARIABLE)
            self.ops.append(param)
            self.ops.append(Op.SET_PARAM)

        old_vars = self.vars # backup vars
        self.vars = set(params)
        self.expression()
        self.ops.append(Op.FN_RET)
        self.vars = old_vars  # restore vars

    def function(self):
        self.consume(TokenType.IDENTIFIER, 'Expect function name')

        name = self.peek(-1).lexeme
        if name in self.vars:
            raise Exception(f'Already defined as variable: {name}')

        params = self.function_params()
        arity = len(params)

        self.consume(TokenType.FN, 'Expect "=>"')

        # function header
        self.ops.append(Op.FN)
        self.ops.append(name)
        self.ops.append(arity)

        jump = self.jump()
        self.function_body(params)
        self.patch_jump(jump)

        self.fns[name] = arity

    def jump(self) -> int:
        i = len(self.ops)
        self.ops.append(-1)
        return i

    def patch_jump(self, i: int):
        self.ops[i] = len(self.ops) - i

    def call(self):
        name = self.peek(-1).lexeme
        arity = self.fns[name]

        for _ in range(arity):
            if self.match(TokenType.EOL):
                raise Exception(f'Wrong number of arguments')
            self.expression()

        self.ops.append(Op.CALL)
        self.ops.append(name)

    def grouping(self):
        if self.match(TokenType.FN_KW):
            raise Exception(f'Function declared within an expression')
        self.expression()
        self.consume(TokenType.RIGHT_PAREN, f'Expect ")" after expression')

    def number(self):
        lexeme = self.peek(-1).lexeme
        self.ops.append(Op.NUMBER)
        cast = float if '.' in lexeme else int
        self.ops.append(cast(lexeme))

    def identifier(self):
        if self.match(TokenType.EQUAL):
            self.variable()
        elif self.peek(-1).lexeme in self.fns:
            self.call()
        else:
            self.get()

    def variable(self):
        name = self.peek(-1).lexeme
        if name in self.fns:
            raise Exception(f'Already defined as function: {name}')
        self.vars.add(name)

        self.ops.append(Op.VARIABLE)
        self.ops.append(name)

    def get(self):
        name = self.peek(-1).lexeme
        if name not in self.vars:
            raise Exception(f'Undefined variable: {name}')
        self.ops.append(Op.GET)
        self.ops.append(name)

    def binary(self):
        type = self.peek(-1).type
        rule = self.rules[type]
        self.parse_precedence(Precedence(rule.precedence+1))
        match type:
            case TokenType.PLUS: self.ops.append(Op.ADD)
            case TokenType.MINUS: self.ops.append(Op.SUB)
            case TokenType.STAR: self.ops.append(Op.MUL)
            case TokenType.SLASH: self.ops.append(Op.DIV)
            case TokenType.PERCENT: self.ops.append(Op.MOD)
            case TokenType.EQUAL: self.ops.append(Op.SET)
            case _: raise Exception(f'Undefined token type: {type}')

    def unary(self):
        type = self.peek(-1).type
        self.parse_precedence(Precedence.UNARY)
        match type:
            case TokenType.MINUS: self.ops.append(Op.NEG)
            case _: raise Exception(f'Undefined token type: {type}')

    def advance(self):
        if self.current+1 < len(self.source):
            self.current += 1

    def peek(self, distance: int = 0) -> Token:
        i = self.current + distance
        return self.source[i]

    def match(self, type: TokenType) -> bool:
        return self.peek().type == type

    def consume(self, type: TokenType, message: str):
        if self.peek().type != type:
            raise Exception(message)
        self.advance()


class VM:
    def __init__(self, debug=False):
        self.stack = []
        self.vars = {}
        self.fns = {}
        self.ops = []
        self.ip = 0
        self.local_vars = {}
        self.fn_call = False
        self.debug = debug

    def eval(self, _ops: list[Value], max_steps=1000):
        if len(_ops) == 0:
            return ''

        self.ip = len(self.ops)
        self.ops += _ops
        self.stack.clear()
        self.local_vars.clear()
        self.fn_call = False

        step = 0
        while self.ip < len(self.ops):
            step+=1
            if step >= max_steps:
                raise Exception(f'The maximum number of steps has been reached')

            op = self.ops[self.ip]

            if self.debug:
                print('+'*10)
                print('step', step)
                print('op', op)
                print('stack', self.stack)
                print('vars', self.vars)
                print('local_vars', self.local_vars)
                print('fns', self.fns)
                print('fn_call', self.fn_call)

            match op:
                case Op.ADD: self.binary(operator.add)
                case Op.SUB: self.binary(operator.sub)
                case Op.MUL: self.binary(operator.mul)
                case Op.DIV: self.binary(operator.truediv)
                case Op.MOD: self.binary(operator.mod)
                case Op.NEG: self.unary(operator.neg)
                case Op.SET: self.binary(self.set)
                case Op.NUMBER | Op.VARIABLE:
                    self.stack.append(self.advance())
                case Op.SET_PARAM:
                    b = self.stack.pop()
                    a = self.stack.pop()
                    self.set_var(b, a)
                case Op.GET:
                    op = self.advance()
                    self.stack.append(self.get_var(op))
                case Op.FN:
                    name = self.advance()
                    arity = self.advance()
                    offset = self.advance()
                    self.fns[name] = (self.ip+1, arity)
                    self.stack.append('')
                    self.ip += offset
                case Op.FN_RET:
                    result = self.stack.pop()
                    self.ip = self.stack.pop()
                    self.stack.append(result)
                    self.fn_call = False
                    self.local_vars.clear()
                case Op.CALL:
                    name = self.advance()
                    offset, arity = self.fns[name]
                    params = self.pop_n(arity)
                    self.stack.append(self.ip)
                    self.stack.extend(params)
                    self.ip = offset-1
                    self.fn_call = True
                case _:
                    print(f'Undefined op: {op}')

            self.ip += 1

        return self.stack.pop()

    def set_var(self, name, value):
        if self.fn_call:
            self.local_vars[name] = value
        else:
            self.vars[name] = value

    def get_var(self, name):
        if self.fn_call:
            return self.local_vars[name]
        else:
            value = self.vars[name]
            while isinstance(value, str):
                value = self.vars[value]
            return value

    def advance(self):
        self.ip += 1
        return self.ops[self.ip]

    def pop_n(self, n: int):
        return [self.stack.pop() for _ in range(n)]

    def set(self, a, b):
        self.set_var(a, b)
        return b

    def binary(self, fn: Callable):
        b = self.stack.pop()
        a = self.stack.pop()
        c = fn(a, b)
        self.stack.append(c)

    def unary(self, fn: Callable):
        a = self.stack.pop()
        c = fn(a)
        self.stack.append(c)


class Interpreter:
    def __init__(self, debug=False):
        self.s = Scanner()
        self.c = Compiler()
        self.v = VM(debug=debug)
        self.debug = debug

    def input(self, expression):
        if self.debug:
            print('expression', expression)
        tokens = self.s.scan(expression)
        if self.debug:
            print('tokens', tokens)
        ops = self.c.compile(tokens)
        if self.debug:
            print('ops', ops)
        return self.v.eval(ops)



def assert_equals(actual, expected, msg=''):
    if actual != expected:
        print(f'ERROR: assert_equals: {msg}\nactual:   {actual}\nexpected: {expected}')


def expect_error(msg, fn):
    try:
        fn()
    except Exception as e:
        print(f'{msg} => {e.__class__.__name__}: {e}')
        return
    print(f'ERROR: expect_error: {msg}')


interpreter = Interpreter(bool(0))


# Basic arithmetic
assert_equals(interpreter.input("1 + 1"), 2)
assert_equals(interpreter.input("1 + 1.234"), 2.234)
assert_equals(interpreter.input("2 - 1"), 1)
assert_equals(interpreter.input("2 * 3"), 6)
assert_equals(interpreter.input("8 / 4"), 2)
assert_equals(interpreter.input("8 / 5"), 1.6)
assert_equals(interpreter.input("7 % 4"), 3)
assert_equals(interpreter.input("1 + 2 + 3"), 6)
assert_equals(interpreter.input("1 * 2 * 3"), 6)
assert_equals(interpreter.input("4 / 2 * 3"), 6)
assert_equals(interpreter.input("---3"), -3)
assert_equals(interpreter.input("3--3"), 6)
assert_equals(interpreter.input("1+2*3"),  7)
assert_equals(interpreter.input("1*2+3"),  5)


# Variables
assert_equals(interpreter.input("x = 1"), 1)
assert_equals(interpreter.input("x"), 1)
assert_equals(interpreter.input("x + 3"), 4)
expect_error("input: 'y'", lambda : interpreter.input("y"))


# Functions
interpreter.input("fn avg x y => (x + y) / 2")
assert_equals(interpreter.input("avg 4 2"), 3)
expect_error("input: 'avg 7'", lambda : interpreter.input("avg 7"))
expect_error("input: 'avg 7 2 4'", lambda : interpreter.input("avg 7 2 4"))

# Conflicts
expect_error("input: 'fn x => 0'", lambda : interpreter.input("fn x => 0"))
expect_error("input: 'avg = 5'", lambda : interpreter.input("avg = 5"))


# Custom
assert_equals(interpreter.input(""), "")
assert_equals(interpreter.input(" "), "")


interpreter.input("fn echo x => x")
interpreter.input("fn add x y => x + y")
assert_equals(interpreter.input("add 3 4"), 7)
assert_equals(interpreter.input("add echo 4 echo 3"), 7)

expect_error("invalid input", lambda : interpreter.input("1 2"))

interpreter.input("fn add x y => x + y")
expect_error("function is called with too many arguments",
             lambda : interpreter.input("avg echo 7 echo 2 echo 4"))


expect_error("duplicate variables names",
             lambda : interpreter.input("fn add x x => x + x"))

expect_error("invalid variable name",
             lambda : interpreter.input("fn add x y => x + z"))

expect_error("function declared within an expression",
             lambda : interpreter.input("(fn f => 1)"))


assert_equals(interpreter.input("x = y = z = 713"), 713)
assert_equals(interpreter.input("x"), 713)
assert_equals(interpreter.input("y"), 713)
assert_equals(interpreter.input("z"), 713)
