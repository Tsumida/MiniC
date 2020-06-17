'''
Copyright: 
Author: 黄涛
Version: 1.0
Date: 2020-04-09
No history version
一个栈，用列表实现，支持最基本的push pop empty top 等操作
'''

# 调用：LRParse(TokenList) TokenList为符号流
class stack:
    def __init__(self):
        self._st = []

    def push(self, obj):
        self._st.append(obj)

    def pop(self):
        if self.empty():
            print("Stack is Empty!")  # ERROR
        else:
            self._st.pop()

    def empty(self):
        return not bool(self._st)

    def top(self):
        if self.empty():
            print("Stack is Empty!")  # ERROR
        else:
            return self._st[-1]