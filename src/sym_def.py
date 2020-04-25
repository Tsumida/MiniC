# -*- coding: UTF-8 -*-

"""
Author: 黄涛
该模块定义了编译器所需的符号，如：
    TokenType, 词法单元类型
    Token, 包含词法单元及其类型
    letters, 字母表

    KEYWORD, 一个字典, 提供TinyC的关键字到其TokenType的元素
    OPERATOR, 一个字典, 提供TinyC的运算符到其TokenType的元素
    DELIMITER, 一个字典, 提供TinyC的界限符到其TokenType的元素

    NonTerminal，非终结符
    ActionKey, 用作LR分析表中的Action表的Key
    ActionVal
    GotoKey, Goto表的key
    BNF, 代表一个产生式
"""


from enum import Enum


class TokenType(Enum):
    ERROR = -1
    OTHERS = -0x3f3f3f3f
    EOF = 0  # EOF
    IF = 1
    ELSE = 2
    INT = 3
    RETURN = 4
    VOID = 5
    WHILE = 6

    PLUS = 7  # +
    MINUS = 8  # -
    TIMES = 9  # *
    OVER = 10  # /
    LT = 11  # <
    LE = 12  # <=
    RT = 13  # >
    RE = 14  # >=
    EQ = 15  # ==
    NEQ = 16  # !=
    ASSIGN = 17  # =
    SEMI = 18  # ;
    COMMA = 19  # ,
    LPAREN, RPAREN = 20, 21  # ()
    LBRACKET, RBRACKET = 22, 23  # []
    LBRACE, RBRACE = 24, 25  # {}

    ID = 26
    NUM = 27

    def __eq__(self, other):
        return self.value == other.value and self.name == other.name


class Token:
    def __init__(self, name, token_type):
        self.name = name
        self.type = token_type

    def __repr__(self):
        # 打印成str, 方便debug
        return f"Token({self.name}, {self.type})"  # f字符串要求py3.5以上

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type


# 字母
letters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-*/<>()[]{}!="

# 保留字
KEYWORD = {'if': TokenType.IF, 'else': TokenType.ELSE,
           'int': TokenType.INT, 'return': TokenType.RETURN,
           'void': TokenType.VOID, "while": TokenType.WHILE
           }

# 运算符
OPERATOR = {'+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.TIMES,
            '/': TokenType.OVER, '<': TokenType.LT, '<=': TokenType.LE,
            '>': TokenType.RT, '>=': TokenType.RE, '==': TokenType.EQ,
            '!=': TokenType.NEQ, '=': TokenType.ASSIGN,
            }
# 界符
DELIMITER = {'{': TokenType.LBRACE, '}': TokenType.RBRACE,
             '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
             '(': TokenType.LPAREN, ')': TokenType.RPAREN,
             ';': TokenType.SEMI, ',': TokenType.COMMA,
             }


# op for LR
class Operation(Enum):
    SHIFT = 0
    REDUCE = 1
    ACCEPT = -1


class NonTerminal(Enum):
    additive_expression = 0
    addop = 1
    arg_list = 2
    args = 3
    call = 4
    compound_stmt = 5
    declaration = 6
    declaration_list = 7
    expression = 8
    expression_stmt = 9
    factor = 10
    fun_declaration = 11
    iteration_stmt = 12
    local_declarations = 13
    mulop = 14
    param = 15
    param_list = 16
    params = 17
    program = 18
    relop = 19
    return_stmt = 20
    selection_stmt = 21
    simple_expression = 22
    statement = 23
    statement_list = 24
    term = 25
    type_specifier = 26
    var = 27
    var_declaration = 28

    def __eq__(self, other):
        return self.value == other.value and self.name == other.name


class GotoKey:
    """
    Goto表的Key
    """
    def __init__(self, stateID, nonTerminalType):
        self.stateID = stateID
        self.nonTerminalType = nonTerminalType

    def __eq__(self, other):
        return self.stateID == other.stateID and self.nonTerminalType == other.nonTerminalType

    def __hash__(self):
        return self.stateID * 1000000000 + self.nonTerminalType.value


class ActionKey:
    """
    Action table的key
    """
    def __init__(self, stateID, tokenType):
        self.stateID = stateID
        self.tokenType = tokenType

    def __eq__(self, other):
        return self.stateID == other.stateID and self.tokenType == other.tokenType

    def __hash__(self):
        return self.stateID * 1000000000 + self.tokenType.value

    def __repr__(self):
        return f"ActionKey({self.stateID}, {self.tokenType})"


class ActionVal:
    """
    Action table的value
    """
    def __init__(self, operation, num):
        self.operation = operation
        self.num = num

    def __repr__(self):
        return f"ActionVal({self.operation}, {self.num})"


class BNF:
    """
    代表一个产生式: symbol -> expression
    """
    def __init__(self, symbol, expression):
        self.symbol = symbol
        self.expression = expression

    def __repr__(self):
        return f"BNF: {self.symbol} -> {self.expression}"

