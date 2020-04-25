"""
author: 黄涛
"""

class TreeNode:
    """
    语法树节点
    character的类型是NonTerminal或者Token
    """
    def __init__(self, character=None):
        self.character = character
        self.children = []
