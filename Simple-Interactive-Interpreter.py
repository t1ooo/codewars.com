# https://www.codewars.com/kata/52ffcfa4aff455b3c2000750

# %%
from enum import Enum

Type = Enum('Type', [
    'PLUS', 'MINUS', 'STAR', 'SLASH', 'PERCENT',
    'EQUAL',
    'FN_OP', 'FN_KW',
    'L_PAREN', 'R_PAREN',
    'IDENTIFIER', 'NUMBER',
])


class Token:
    def __init__(self, type: Type, lexeme: str = ''):
        self.type = type
        self.lexeme = lexeme

    def __repr__(self):
        return f'({self.__class__.__name__} {self.type} {self.lexeme})'


class Scanner:
    def __init__(self):
        self.set_source('')

    def set_source(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0

    def scan(self, source: str) -> list[Token]:
        self.set_source(source)

        tokens = []
        while not self.is_at_end():
            token = self.scan_token()
            if token is not None:
                tokens.append(token)
        return tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> Token|None:
        self.start = self.current
        c = self.advance()

        if c == ' ': return None
        if c == '+': return Token(Type.PLUS)
        if c == '-': return Token(Type.MINUS)
        if c == '*': return Token(Type.STAR)
        if c == '/': return Token(Type.SLASH)
        if c == '%': return Token(Type.PERCENT)
        if c == '(': return Token(Type.L_PAREN)
        if c == ')': return Token(Type.R_PAREN)
        if c == '=': return self.equal()

        if self.is_alpha(c): return self.identifier()
        if self.is_digit(c): return self.number()

        raise Exception(f'Undefined token: {c}')

    def equal(self) -> Token:
        if self.peek() == '>':
            self.advance()
            return Token(Type.FN_OP)
        return Token(Type.EQUAL)

    def is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'

    def is_alpha(self, c: str) -> bool:
        str.isalnum
        return ('a' <= c <= 'z') \
            or ('A' <= c <= 'Z') \
            or c == '_'

    def number(self) -> Token:
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == '.':
            self.advance()
            return self.number()

        return Token(Type.NUMBER, self.lexeme())

    def identifier(self) -> Token:
        while self.is_alpha(self.peek()) \
              or self.is_digit(self.peek()):
            self.advance()

        lexeme = self.lexeme()
        type = Type.FN_KW if lexeme == 'fn' else Type.IDENTIFIER
        return Token(type, lexeme)

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def advance(self) -> str:
        c = self.peek()
        self.current += 1
        return c

    def lexeme(self) -> str:
        return self.source[self.start:self.current]


class Visitor:
    def visit_literal(self, expr: 'Literal'): pass
    def visit_variable(self, expr: 'Variable'): pass
    def visit_assignment(self, expr: 'Assignment'): pass
    def visit_group(self, expr: 'Group'): pass
    def visit_call(self, expr: 'Call'): pass
    def visit_fn(self, expr: 'Fn'): pass
    def visit_binary(self, expr: 'Binary'): pass
    def visit_unary(self, expr: 'Unary'): pass


class Expr:
    def accept(self, visitor: Visitor):
        pass


class Literal(Expr):
    def __init__(self, value: int|float):
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_literal(self)

    def __repr__(self):
        return f'({self.__class__.__name__} {self.value})'


class Variable(Expr):
    def __init__(self, name: str):
        self.name = name

    def accept(self, visitor: Visitor):
        return visitor.visit_variable(self)

    def __repr__(self):
        return f'({self.__class__.__name__} {self.name})'


class Assignment(Expr):
    def __init__(self, name: str, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_assignment(self)

    def __repr__(self):
        return f'({self.__class__.__name__} {self.name} {self.value})'


class Group(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor: Visitor):
        return visitor.visit_group(self)

    def __repr__(self):
        return f'({self.__class__.__name__} {self.expr})'


class Call(Expr):
    def __init__(self, name: str, args: list[Expr]):
        self.name = name
        self.args = args

    def accept(self, visitor: Visitor):
        return visitor.visit_call(self)

    def __repr__(self):
        return f'({self.__class__.__name__} {self.name} {self.args})'


class Fn(Expr):
    def __init__(self, name: str, params: list[str], body: Expr):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: Visitor):
        return visitor.visit_fn(self)

    def arity(self):
        return len(self.params)

    def __repr__(self):
        return f'({self.__class__.__name__} {self.name} {self.params}: {self.body})'


class Binary(Expr):
    def __init__(self, left: Expr, op: Token, right: Expr):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visit_binary(self)

    def __repr__(self):
        return f'({self.__class__.__name__} {self.left} {self.op} {self.right})'


class Unary(Expr):
    def __init__(self, op: Token, right: Expr):
        self.op = op
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visit_unary(self)

    def __repr__(self):
        return f'({self.__class__.__name__} {self.op} {self.right})'


class Parser:
    def __init__(self):
        self.fns = {}
        self.vars = {}
        self.set_tokens([])

    def set_tokens(self, tokens: list[Token]):
        self.tokens = tokens
        self.start = 0
        self.current = 0

    def parse(self, tokens: list[Token]):
        self.set_tokens(tokens)

        if self.match(Type.FN_KW):
            return self.function()

        expr = self.expression()
        if not self.is_at_end():
            raise Exception(f'Invalid input: parsed:{expr}, remainder:{self.tokens[self.current:]}')

        return expr

    def expression(self) -> Expr:
        expr = self.binary()

        while self.match(Type.PLUS, Type.MINUS):
            op = self.advance()
            right = self.binary()
            expr = Binary(expr, op, right)

        return expr

    def binary(self) -> Expr:
        expr = self.unary()

        while self.match(Type.STAR, Type.SLASH, Type.PERCENT):
            op = self.advance()
            right = self.unary()
            expr = Binary(expr, op, right)

        return expr

    def unary(self) -> Expr:
        if self.match(Type.MINUS):
            op = self.advance()
            right = self.unary()
            return Unary(op, right)

        return self.factor()

    def function(self) -> Expr:
        self.advance()
        if not self.match(Type.IDENTIFIER):
            raise Exception(f'Expect function name')

        name = self.advance().lexeme
        if name in self.vars:
            raise Exception(f'Already defined as variable: {name}')

        params = []
        while self.match(Type.IDENTIFIER):
            param = self.advance().lexeme
            if param in params:
                raise Exception(f'Duplicate function param names: {param}')
            params.append(param)

        if not self.match(Type.FN_OP):
            raise Exception(f'Expect =>')

        self.advance()

        prev_vars = self.vars
        self.vars = params
        body = self.expression()
        self.vars = prev_vars

        fn = Fn(name, params, body)
        self.fns[name] = fn

        return fn

    def factor(self) -> Expr:
        if self.match(Type.NUMBER):
            return self.number()

        if self.match(Type.IDENTIFIER):
            name = self.advance().lexeme
            if self.match(Type.EQUAL):
                return self.assignment(name)
            if name in self.fns:
                return self.call(name)
            if name not in self.vars:
                raise Exception(f'Undefined variable: {name}')
            return Variable(name)

        if self.match(Type.L_PAREN):
            return self.group()

        raise Exception(f'Invalid input')

    def number(self) -> Expr:
        token = self.advance()
        cast_to = float if '.' in token.lexeme else int
        return Literal(cast_to(token.lexeme))

    def call(self, name) -> Expr:
        args = []
        for _ in range(self.fns[name].arity()):
            args.append(self.expression())
        return Call(name, args)

    def assignment(self, name) -> Expr:
        if name in self.fns:
            raise Exception(f'Already defined as function: {name}')

        self.advance()
        expr = self.expression()
        var = Assignment(name, expr)
        self.vars[name] = var
        return var

    def group(self) -> Expr:
        self.advance()
        expr = self.expression()
        if not self.match(Type.R_PAREN):
            raise Exception(f'Expect )')
        self.advance()
        return Group(expr)

    def match(self, *types: Type) -> bool:
        token = self.maybe_peek()
        if token is None:
            return False
        for type in types:
            if token.type == type:
                return True
        return False

    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)

    def maybe_peek(self) -> Token|None:
        # return self.char(self.current)
        if self.is_at_end():
            return None
        return self.tokens[self.current]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def advance(self) -> Token:
        c = self.peek()
        self.current += 1
        return c


class Eval(Visitor):
    def __init__(self):
        self.env: dict[str, object] = {}

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visit_literal(self, expr: 'Literal'):
        return expr.value

    def visit_variable(self, expr: 'Variable'):
        return self.env[expr.name]

    def visit_assignment(self, expr: 'Assignment'):
        value = self.evaluate(expr.value)
        self.env[expr.name] = value
        return value

    def visit_group(self, expr: 'Group'):
        return self.evaluate(expr.expr)

    def visit_call(self, expr: 'Call'):
        fn = self.env[expr.name]
        if not isinstance(fn, Fn):
            raise Exception(f'Not a function: {expr.name}')
        args = [self.evaluate(arg) for arg in expr.args]
        
        prev_env = self.env
        self.env = dict(zip(fn.params, args))
        result = self.evaluate(fn.body)
        self.env = prev_env
        
        return result

    def visit_fn(self, expr: 'Fn'):
        self.env[expr.name] = expr
        return ''

    def visit_binary(self, expr: 'Binary'):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if not isinstance(left, (int, float)):
            raise Exception(f'Unsupported operation: {left}({type(left)})')

        if not isinstance(right, (int, float)):
            raise Exception(f'Unsupported operation: {right}({type(right)})')

        if expr.op.type == Type.PLUS: return left + right
        if expr.op.type == Type.MINUS: return left - right
        if expr.op.type == Type.STAR: return left * right
        if expr.op.type == Type.SLASH: return left / right
        if expr.op.type == Type.PERCENT: return left % right

        raise Exception(f'Unsupported binary operation: {expr.op}')

    def visit_unary(self, expr: 'Unary'):
        right = self.evaluate(expr.right)

        if not isinstance(right, (int, float)):
            raise Exception(f'Unsupported operation: {right}({type(right)})')

        if expr.op.type == Type.MINUS: return -right

        raise Exception(f'Unsupported unary operation: {expr.op}')


class Interpreter:
    def __init__(self, debug=False):
        self.s = Scanner()
        self.p = Parser()
        self.e = Eval()
        self.debug = debug

    def input(self, expression):
        if self.debug:
            print('expression', expression)
        tokens = self.s.scan(expression)
        if self.debug:
            print('tokens', tokens)
        if len(tokens) == 0:
            return ''
        ast = self.p.parse(tokens)
        if self.debug:
            print('ast', ast)
        return self.e.evaluate(ast)


def assert_equals(actual, expected, msg=''):
    if actual != expected:
        print(f'ERROR: assert_equals: {msg}\nactual:   {actual}\nexpected: {expected}')


def expect_error(msg, fn):
    try:
        fn()
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        return
    print(f'ERROR: expect_error: {msg}')


interpreter = Interpreter(False)


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
