# -*- coding: UTF-8 -*-
from enum import Enum


class TokenType(Enum):
    ERROR = -1
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
