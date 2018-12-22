import math
from enum import Enum

def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

def tan(x):
    return math.tan(x)

def log(x):
    return math.log(x)

def exp(x):
    return math.exp(x)

def sqrt(x):
    return math.sqrt(x)

class Token_Type(Enum):
    ORIGIN = 0
    SCALE = 1
    ROT = 2
    IS = 3
    TO = 4
    STEP = 5
    DRAW = 6
    FOR = 7
    FROM = 8
    T = 9
    SEMICO = 10
    L_BRACKET = 11
    R_BRACKET = 12
    COMMA = 13
    PLUS = 14
    MINUS = 15
    MUL = 16
    DIV = 17
    POWER = 18
    FUNC = 19
    CONST_ID = 20
    NONTOKEN = 21
    ERRTOKEN = 22
    COMMENT = 23

TokenTab = [
    [Token_Type.CONST_ID, "PI", 3.1415926, None],
    [Token_Type.CONST_ID, "E", 2.71828, None],
    [Token_Type.T, "T", 0.0, None],
    [Token_Type.FUNC, "SIN", 0.0, sin],
    [Token_Type.FUNC, "COS", 0.0, cos],
    [Token_Type.FUNC, "TAN", 0.0, tan],
    [Token_Type.FUNC, "LN", 0.0, log],
    [Token_Type.FUNC, "EXP", 0.0, exp],
    [Token_Type.FUNC, "SQRT", 0.0, sqrt],
    [Token_Type.ORIGIN, "ORIGIN", 0.0, None],
    [Token_Type.SCALE, "SCALE", 0.0, None],
    [Token_Type.ROT, "ROT", 0.0, None],
    [Token_Type.IS, "IS", 0.0, None],
    [Token_Type.FOR, "FOR", 0.0, None],
    [Token_Type.FROM, "FROM", 0.0, None],
    [Token_Type.TO, "TO", 0.0, None],
    [Token_Type.STEP, "STEP", 0.0, None],
    [Token_Type.DRAW, "DRAW", 0.0, None]
]

class Token:
    def __init__(self, type, lexeme, value, func):
        """
        :param type: 类别
        :param lexeme: 属性，原始输入的字符串
        :param value: 属性，若记号是常数则是常数值
        :param func: 属性，若记号是函数则是函数
        """
        self.type = type
        self.lexeme = lexeme
        self.value = value
        self.func = func