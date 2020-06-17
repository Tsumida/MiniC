from action_table import *
from goto_table import *
from BNF import *
from stack import *
from tree_node import *
import lexer
from sym_def import Token, Operation, ActionVal, ActionKey, GotoKey
'''
Copyright: 
Author: 黄涛
Version: 1.0
Date: 2020-04-09
No history version
语法分析 生成具体语法树
'''

# 调用：LRParse(TokenList) TokenList为符号流
def LRParse(TokenList):
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
            print("UNEXPECTED TOKEN: {} {}".format(token.name,pos))
            break
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
                    print("UNKOWUN GOTO KEY: ", NowGotoKey.stateID, NowGotoKey.nonTerminalType)
            # 接受
            else:
                return CharacterStack.top()
    return None


def dfs(root: TreeNode, dep: int):
    if root is None:
        return
    print(" " * dep, end="")
    print(root.character)
    for chl in root.children:
        dfs(chl, dep + 1)

