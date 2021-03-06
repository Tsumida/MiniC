"""
Author: 黄涛
"""

from action_table import *
from goto_table import *
from BNF import *
from stack import *
from tree_node import *
from lexer import *
from sym_def import Token, Operation, ActionVal, ActionKey, GotoKey


class SyntaxTree:
    """
    语法树类
    """
    def __init__(self, root=None):
        self.root = root

    def dfs_print(self):
        def dfs(root: TreeNode, dep: int):
            if root is None:
                return
            print("    " * dep, end="")
            print(root.character)
            for chl in root.children:
                dfs(chl, dep + 1)
        return dfs(self.root, 0)


class LRParsingErr(Exception):
    """
    错误类，包含了提示信息，出错的位置和符号
    """
    def __init__(self, pos: int, sym, msg: str):
        self.pos = pos  # index of sym in TokenList.
        self.sym = sym  # token or non-terminal
        self.msg = msg

    def __repr__(self):
        return f"LRParsingErr:pos={self.pos}, sym={self.sym}, msg={self.msg}"


def LRParse(TokenList: List[Token]) -> SyntaxTree:
    """
    对Token序列进行LR(1)分析, 生成对应的语法树
    :param TokenList:
    :return:
    """
    StateStack = stack()  # 状态栈
    CharacterStack = stack()  # 符号栈
    StateStack.push(0)  # 初始状态
    pos = 0

    while pos < len(TokenList):  # 遍历每个Token
        token = TokenList[pos]
        flag = False  # 判断这个Actionkey在不在Action表，不在就报错
        NowActionKey = ActionKey(StateStack.top(), token.type)
        if NowActionKey in ActionTable:
            NowActionVal = ActionTable[NowActionKey]
            flag = True
        elif ActionKey(StateStack.top(), TokenType.OTHERS) in ActionTable:
            NowActionVal = ActionTable[ActionKey(StateStack.top(), TokenType.OTHERS)]
            flag = True
        else:
            raise LRParsingErr(pos, NowActionKey, "unexpected token")
        if flag:
            action, ID = NowActionVal.operation, NowActionVal.num
            # print(action, ID)
            # 移进
            if action == Operation.SHIFT:  # 此时ID代表将要移进的状态
                StateStack.push(ID)
                CharacterStack.push(TreeNode(token))
                pos += 1
            # 规约
            elif action == Operation.REDUCE:  # 此时ID代表将要规约的产生式
                ReduceExp = ExpressionTable[ID]  # 当前产生式
                ReduceExpLen = len(ReduceExp.expression)  # 产生式后面部分的长度
                NonTerminalTreeNode = TreeNode(ReduceExp.symbol)  # 产生一个节点，代表当前终结符/非终结符
                for i in range(ReduceExpLen):
                    StateStack.pop()
                    NonTerminalTreeNode.children.append(CharacterStack.top())  # 从符号栈和状态中的内容取出len个，记录符号栈取出的内容
                    CharacterStack.pop()
                NowGotoKey = GotoKey(StateStack.top(), ReduceExp.symbol)
                NonTerminalTreeNode.children.reverse()  # 出栈顺序是逆序，需要反转
                if NowGotoKey in GotoTable:
                    StateStack.push(GotoTable[NowGotoKey])  # 查找goto表是否有符合要求的Key
                    CharacterStack.push(NonTerminalTreeNode)
                else:
                    raise LRParsingErr(pos, NowGotoKey, "unknown goto key")
            # 接受
            else:
                return SyntaxTree(CharacterStack.top())
    return SyntaxTree()
