
'''
Copyright: 
Author: 黄涛
Version: 1.0
Date: 2020-04-13
No history version
节点类
'''

# 生成具体语法树的节点类
class TreeNode:
    def __init__(self, character=None):
        self.character = character
        self.children = []

# 生成抽象语法树的节点类
class nTreeNode:
    def __init__(self, kind=None, character=None):
        self.kind = kind # 操作类型
        self.character = character # 代表的具体符号，比如变量名，函数名，操作符等
        self.children = [] # 子节点
        self.sibling = [] # 兄弟节点
        # 以下为属性文法中的域
        self.type = '' # 类型
        self.val = 0 # 变量值
        self.isarray = 0 # 是否为数组类型
