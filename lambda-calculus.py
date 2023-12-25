# %%
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
def NONE(a):
    return lambda b: b
def TRUE(a):
    return lambda b: a
def FALSE(a):
    return lambda b: b
def NOT(a):
    return a(FALSE)(TRUE)
def OR(a):
    def second(b):
        return b(TRUE)(a)
    return second
def AND(a):
    def second(b):
        return b(a)(FALSE)
    return second

def ZERO(x):
    return lambda i: i
def INC(x):
    return lambda i: x
def ONE(x):
    return INC(ZERO)
def DEC(x):
    return x(NONE)(NONE)
def TWO(x):
    return INC(ONE)
def THREE(x):
    return INC(TWO)
def FOUR(i):
    return INC(THREE)
assert DEC(ONE) is ZERO
assert DEC(TWO) is ONE
assert DEC(DEC(TWO)) is ZERO
# The number can be something, that can be callen n times. n'th call returns PAIR(FALSE, NONE), everithing else returns PAIR(TRUE, underlying func)
# TODO: Add addition, substraction, multiplication, eq may be hard
# TODO: is it possible to have meaningful default preint repr like <lambda>.<lambda>...

def ZERO(x):
    return lambda y: y
def ONE(f):
    return lambda v: f(v)
def TWO(x):
    return lambda y: x(x(y))
def THREE(x):
    return lambda y: x(x(x(y)))
def FOUR(x):
    return lambda y: x(x(x(x(y))))
def incr(x):
    return x + 1
assert ZERO(incr)(0) == 0
assert ONE(incr)(0) == 1
assert TWO(THREE)(incr)(0) == 9
assert TWO(FOUR)(incr)(0) == 16
assert FOUR(THREE)(incr)(0) == 81

def INC(n):
    return lambda f: lambda v: f(n(f)(v))
def ONE(f):
    return INC(ZERO)(f)
def TWO(f):
    return INC(ONE)(f)
def THREE(f):
    return INC(TWO)(f)
def FOUR(f):
    return INC(THREE)(f)
assert ZERO(incr)(0) == 0
assert ONE(incr)(0) == 1
assert TWO(THREE)(incr)(0) == 9
assert TWO(FOUR)(incr)(0) == 16
assert FOUR(THREE)(incr)(0) == 81

def ADD(n1):
    def second(n2):
        return n2(INC)(n1)
    return second
assert ADD(ONE)(TWO)(incr)(0) == 3
assert ADD(FOUR)(TWO)(incr)(0) == 6
def ALTADD(n1):
    def second(n2):
        return lambda f: lambda v: n2(f)(n1(f)(v))
    return second
assert ALTADD(ONE)(TWO)(incr)(0) == 3
assert ALTADD(FOUR)(TWO)(incr)(0) == 6
TWICE = lambda n: TWO(ADD)(n)
# def TWICE(n):
#     return TWO(ADD)(n)
assert ADD(THREE)(TWO)(incr)(0) == 5

def TWICE(n):
    return TWO(ADD(n))(ZERO)
assert TWICE(TWO)(incr)(0) == 4
assert TWICE(THREE)(incr)(0) == 6
def MUL(n1):
    def second(n2):
        return n2(ADD(n1))(ZERO)
    return second
assert MUL(ONE)(TWO)(incr)(0) == 2
assert MUL(FOUR)(TWO)(incr)(0) == 8
def SQUARE(n):
    return TWO(MUL(n))(ONE)
assert SQUARE(ZERO)(incr)(0) == 0
assert SQUARE(ONE)(incr)(0) == 1
assert SQUARE(TWO)(incr)(0) == 4
def POW(n1):
    def second(n2):
        return n2(MUL(n1))(ONE)
    return second
assert POW(ZERO)(TWO)(incr)(0) == 0
assert POW(TWO)(ZERO)(incr)(0) == 1
assert POW(ONE)(TWO)(incr)(0) == 1
assert POW(FOUR)(TWO)(incr)(0) == 16
# Alternative thinking: a number is a function which applyes f to v
# Thus multiplication gives a function which applyes f to v by generating a function(i) which applyes f to i, and applying that generated function n2 times to v
def ALTMUL(n1):
    def second(n2):
        # return lambda f: lambda v: n2(lambda i: n1(f)(i))(v)
        # Collapsed version:
        return lambda f: n2(n1(f))
    return second
assert ALTMUL(ONE)(TWO)(incr)(0) == 2
assert ALTMUL(FOUR)(TWO)(incr)(0) == 8

def SQUARE(n):
    return lambda f: lambda v: n(lambda i: n(f)(i))(v)
assert SQUARE(ONE)(incr)(0) == 1
assert SQUARE(TWO)(incr)(0) == 4
assert SQUARE(THREE)(incr)(0) == 9
def CUBE(n):
    return lambda f: lambda v: n(lambda j: n(lambda i: n(f)(i))(j))(v)
assert CUBE(ONE)(incr)(0) == 1
assert CUBE(TWO)(incr)(0) == 8
assert CUBE(THREE)(incr)(0) == 27
# Apply n2 times the function n1 to f to v
# Applying function n1 to f to v means applying f to v n1 times
# So ALTPOW translates to "apply n2 times a thing that applyes f to v n1 times to itself":
# n1(lambda n1( lambda n1(...lambda n1(f(v))))) - n2 times do n1 nested calls
def ALTPOW(n1):
    def second(n2):
        return n2(n1)
    return second
assert ALTPOW(ZERO)(TWO)(incr)(0) == 0
assert ALTPOW(TWO)(ZERO)(incr)(0) == 1
assert ALTPOW(ONE)(TWO)(incr)(0) == 1
assert ALTPOW(THREE)(TWO)(incr)(0) == 9
assert ALTPOW(FOUR)(TWO)(incr)(0) == 16
assert ALTPOW(FOUR)(ONE)(incr)(0) == 4

def PAIR(a):
    def second(b):
        return lambda rule: rule(a)(b)
    return second
def FIRST(p):
    return p(TRUE)
def SECOND(p):
    return p(FALSE)
t = PAIR(TWO)(FOUR)
assert FIRST(t) is TWO
assert SECOND(t) is FOUR

def DEC(n):
    def tupler(p):
        return PAIR(INC(FIRST(p)))(FIRST(p))
    return SECOND(n(tupler)(PAIR(ZERO)(ZERO)))
assert DEC(ONE)(incr)(0) == 0
assert DEC(FOUR)(incr)(0) == 3

def ISZERO(n):
    def tester(v):
        return FALSE
    return n(tester)(TRUE)
assert ISZERO(ZERO) is TRUE
assert ISZERO(ONE) is FALSE
assert ISZERO(TWO) is FALSE

def ONLY_FIRST_ISZERO(n1):
    def second(n2):
        return AND(ISZERO(n1))(NOT(ISZERO(n2)))
    return second
assert ONLY_FIRST_ISZERO(ZERO)(TWO) is TRUE
assert ONLY_FIRST_ISZERO(TWO)(ZERO) is FALSE

def ONLY_ONE_ISZERO(n1):
    def second(n2):
        return OR(ONLY_FIRST_ISZERO(n1)(n2))(ONLY_FIRST_ISZERO(n2)(n1))
    return second
assert ONLY_ONE_ISZERO(ZERO)(ZERO) is FALSE
assert ONLY_ONE_ISZERO(ZERO)(ONE) is TRUE
assert ONLY_ONE_ISZERO(TWO)(ONE) is FALSE

def BOTH_NOT_ZERO(n1):
    def second(n2):
        return AND(NOT(ISZERO(n1)))(NOT(ISZERO(n2)))
    return second
assert BOTH_NOT_ZERO(ONE)(ZERO) is FALSE
assert BOTH_NOT_ZERO(ONE)(TWO) is TRUE

def DEC_PAIR(p):
    return PAIR(DEC(FIRST(p)))(DEC(SECOND(p)))
assert FIRST(DEC_PAIR(PAIR(ONE)(TWO))) is ZERO
assert SECOND(DEC_PAIR(PAIR(ONE)(TWO)))(incr)(0) == 1

def PAIR_BOTH_NOT_ZERO(p):
    return BOTH_NOT_ZERO(FIRST(p))(SECOND(p))
assert PAIR_BOTH_NOT_ZERO(PAIR(ZERO)(ONE)) is FALSE
assert PAIR_BOTH_NOT_ZERO(PAIR(TWO)(THREE)) is TRUE

def SAFE_DEC(p):
    return PAIR_BOTH_NOT_ZERO(p)(DEC_PAIR(p))(FALSE)
assert SAFE_DEC(PAIR(ZERO)(ONE)) is FALSE
assert FIRST(SAFE_DEC(PAIR(TWO)(ONE)))(incr)(0) == 1

def identity(i):
    return i
def pair_minus_n(p, n):
    return n(
        lambda cur_pair: PAIR_BOTH_NOT_ZERO(cur_pair)(DEC_PAIR)(identity)(cur_pair)
    )(p)
assert FIRST(pair_minus_n(PAIR(TWO)(ONE), TWO))(incr)(0) == 1
def eq(a, b):
    return AND(ISZERO(FIRST(pair_minus_n(PAIR(a)(b), a))))(ISZERO(SECOND(pair_minus_n(PAIR(a)(b), a))))
assert eq(ONE, ONE) is TRUE
assert eq(TWO, ONE) is FALSE
assert eq(ZERO, ZERO) is TRUE
assert eq(POW(FOUR)(FOUR), ZERO) is FALSE
assert eq(POW(FOUR)(FOUR), POW(FOUR)(FOUR)) is TRUE
assert eq(POW(FOUR)(FOUR), POW(THREE)(THREE)) is FALSE
