# -*- coding: UTF-8 -*-
import re
from enum import Enum, unique


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
    def __init__(self, name, type):
        self.name = name
        self.type = type


# 字母
letters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-*/<>()[]{}!="

# 保留字
keyWord = {'if': TokenType.IF, 'else': TokenType.ELSE,
           'int': TokenType.INT, 'return': TokenType.RETURN,
           'void': TokenType.VOID, "while": TokenType.WHILE
           }

# 运算符
operator = {'+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.TIMES,
            '/': TokenType.OVER, '<': TokenType.LT, '<=': TokenType.LE,
            '>': TokenType.RT, '>=': TokenType.RE, '==': TokenType.EQ,
            '!=': TokenType.NEQ, '=': TokenType.ASSIGN,
            }
# 界符
delimiters = {'{': TokenType.LBRACE, '}': TokenType.RBRACE,
              '[': TokenType.LBRACKET, ']': TokenType.RBRACKET,
              '(': TokenType.LPAREN, ')': TokenType.RPAREN,
              ';': TokenType.SEMI, ',': TokenType.COMMA,
              }
