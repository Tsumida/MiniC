# -*- coding: UTF-8 -*-
import re
from enum import Enum, unique


class TokenType(Enum):
    ERROR = -1  #
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


# 字母
letters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-*/<>()[]{}!=_"
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


# 去掉注释、空行
def filterResource(oldFileName, newFileName):
    f2 = open(newFileName, 'w+')
    code = ''.join(open(oldFileName, 'r').readlines())
    newcode = re.sub(r"/\*([^\*]|(\*)*[^\*/])*(\*)*\*/", "", code)  # 去掉注释/*     */
    for line in newcode.split('\n'):
        line = line.strip()  # 对每行判断是否空
        line = line.replace('\\t', '')
        line = line.replace('\\n', '')
        if not line:
            continue
        else:
            f2.write(line + '\n')
    f2.close()


# 扫描每个单词
def scan(oldFileName, newFileName):
    lines = open(oldFileName, 'r').readlines()
    token = []  # 所有代码的token流二元组
    for line in lines:
        word = ''
        wordTable = []  # 这一行代码的token流二元组
        i = 0
        while i < len(line):
            #    # if(line[i] not in letters)
            #    #语言中不存在这个字符 抛出错误
            #    continue
            word += line[i]
            if line[i] == ' ' or line[i] in delimiters or line[i] in operator:
                if word[0].isalpha() or word[0] == '_':
                    word = word[:-1]
                    if word in keyWord:
                        # 保留字
                        wordTable.append({word: keyWord[word]})
                    else:
                        # 标识符
                        wordTable.append({word: TokenType.ID})
                elif word[:-1].isdigit():
                    # 是整数
                    wordTable.append({word[:-1]: TokenType.NUM})
                if line[i] in delimiters:
                    # 是界符
                    wordTable.append({line[i]: delimiters[line[i]]})
                elif line[i] in operator:
                    # 是运算符
                    s = line[i] + line[i + 1]
                    if s in operator:
                        # 贪心匹配占两个字节的运算符
                        wordTable.append({s: operator[s]})
                        i += 1
                    else:
                        # 只占一个字节的运算符
                        wordTable.append({line[i]: operator[line[i]]})
                word = ''
            i += 1

        token += wordTable
    token += [{"$": TokenType.EOF}]  # 整个代码程序的终结符
    f1 = open(newFileName, 'w')
    for u in token:
        for v in u:
            f1.write("{: <7} {}\n".format(v, u[v]))
    f1.close()


def main(codeFile, tokenFile):
    filterResource(codeFile, 'tmp.txt')
    scan('tmp.txt', tokenFile)


main("r.txt", "token.txt")
# 第一个参数读入代码文件 第二个参数输出Token流文件
