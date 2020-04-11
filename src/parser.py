# 2020-04-11
from typing import List
from unittest import TestCase
from src.sym_def import *

class TokenSeq:
    """
    对token列表的封装.
    """
    def __init__(self, tks: List[Token]):
        self.tks = tks
        self.index = -1

    def next(self):
        """
        取得下一个元素, 并且会推进index
        :return:
        """
        self.index += 1
        if self.index < len(self.tks):
            return self.tks[self.index]
        else:
            return None

    def peek(self):
        """
        用于查看下一个符号，但是不推进index.
        :return:
        """
        if self.index + 1 < len(self.tks):
            return self.tks[self.index + 1]
        else:
            return None


