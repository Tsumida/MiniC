# -*- coding: UTF-8 -*-

"""
Author: 黄涛
该模块包含了词法分析程序和相关函数。
"""
import re
from unittest import TestCase, skipIf
from typing import List  # 给IDE提供类型提示, 无实质影响

from sym_def import *


def filterResource(oldFileName):
    """
    预处理, 去掉注释、空行.
    :param oldFileName:
    :return:
    """
    ncode = ''
    code = ''.join(open(oldFileName, 'r').readlines())
    newCode = re.sub(r"/\*([^\*]|(\*)*[^\*/])*(\*)*\*/", "", code)  # 去掉注释/*     */
    for line in newCode.split('\n'):
        line = line.strip()  # 对每行判断是否空
        line = line.replace('\\t', '')
        line = line.replace('\\n', '')
        if not line:
            continue
        else:
            ncode += line + '\n'
    return ncode


def scan(code: str) -> List[Token]:
    """
    扫描每个单词, 产生token序列
    :param code:
        code是经过预处理的文本。
    :return:
        返回token序列, 元素为Token
    """
    lines = code.split('\n')
    token = []  # 所有代码的token流二元组
    for line in lines:
        word = ''
        line += '\n'
        wordTable = []  # 这一行代码的token流二元组
        i = 0
        while i < len(line):
            #    # if(line[i] not in letters)
            #    #语言中不存在这个字符 抛出错误
            #    continue
            word += line[i]
            if line[i] == ' ' or line[i] == '!' or line[i] == '\n' or line[i] in DELIMITER or line[i] in OPERATOR:
                if word[0].isalpha():
                    word = word[:-1]
                    if word in KEYWORD:
                        # 保留字
                        wordTable.append(Token(word, KEYWORD[word]))
                    else:
                        # 标识符
                        wordTable.append(Token(word, TokenType.ID))
                elif word[:-1].isdigit():
                    # 是整数
                    wordTable.append(Token(word[:-1], TokenType.NUM))
                if line[i] in DELIMITER:
                    # 是界符
                    wordTable.append(Token(line[i], DELIMITER[line[i]]))
                elif line[i] in OPERATOR or line[i] == '!':
                    # 是运算符
                    s = line[i] + line[i + 1]
                    if s in OPERATOR:
                        # 贪心匹配占两个字节的运算符
                        wordTable.append(Token(s, OPERATOR[s]))
                        i += 1
                    elif line[i] in OPERATOR:
                        # 只占一个字节的运算符
                        wordTable.append(Token(line[i], OPERATOR[line[i]]))
                    # else:
                    # print("UNKNOWN TOKEN: ",line[i] )

                word = ''
            i += 1
        token += wordTable
    token.append(Token("$", TokenType.EOF))  # 整个代码程序的终结符
    # print(token)
    return token


def lex(codeFile):
    code = filterResource(codeFile)
    return scan(code)


class TestScan(TestCase):
    """
    单元测试
    """
    @skipIf(True, "")
    def test_single_token(self):
        """
        能够单独解析每个单词
        :return:
        """
        def test(label: str, dic: dict):
            print("testing --- ", label)
            for k, v in dic.items():
                res = scan(k)
                assert res[0].type == v, "Err: input={}, expected {}, got {}".format(k, v, res[0].type)

        test("keyword", KEYWORD)
        test("operator", OPERATOR)
        test("delimiter", DELIMITER)

    @skipIf(True, "")
    def test_statement(self):
        """
        把语句解析为Token列表
        :return:
        """
        def test(label: str, state: str, ans: List[Token]):
            print("testing --- ", label)
            res = scan(state)
            assert res == ans, "Err: \ninput={}\nexpected {}\ngot {}\n".format(
                state, ans, res
            )

        test(
            "assignment",
            "a != b",
            [Token("a", TokenType.ID), Token("!=", TokenType.NEQ), Token("b", TokenType.ID), Token("$", TokenType.EOF)]
        )

        test(
            "if statement",
            "if ( a != b ) return b ;",
            [
                Token("if", TokenType.IF), Token("(", TokenType.LPAREN),
                Token("a", TokenType.ID), Token("!=", TokenType.NEQ), Token("b", TokenType.ID),
                Token(")", TokenType.RPAREN),
                Token("return", TokenType.RETURN), Token("b", TokenType.ID), Token(";", TokenType.SEMI),
                Token("$", TokenType.EOF)
            ]
        )

