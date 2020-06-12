from action_table import *
from goto_table import *
from BNF import *
from stack import *
from tree_node import *
import lexer
import BuildSymTab
from sym_def import Token, Operation, ActionVal, ActionKey, GotoKey, Kind


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
            print("TokenType Error: Unexpected token: {} {}".format(token.name, pos))
            break
        if flag:
            action, ID = NowActionVal.operation, NowActionVal.num
            # 移进
            if action == Operation.SHIFT:  # 此时ID代表将要移进的状态
                StateStack.push(ID)
                CharacterStack.push(nTreeNode(character=token))
                pos += 1
            # 规约
            elif action == Operation.REDUCE:  # 此时ID代表将要规约的产生式
                ReduceExp = ExpressionTable[ID]  # 当前产生式
                ReduceExpLen = len(ReduceExp.expression)  # 产生式后面部分的长度
                tmpTreeNode = nTreeNode()  # 产生一个节点，代表当前终结符/非终结符
                tmpChildList = []
                for i in range(ReduceExpLen):
                    StateStack.pop()
                    tmpChildList.append(CharacterStack.top())  # 从符号栈和状态中的内容取出len个，记录符号栈取出的内容
                    CharacterStack.pop()
                NowGotoKey = GotoKey(StateStack.top(), ReduceExp.symbol)
                tmpChildList.reverse()  # 出栈顺序是逆序，需要反转

                # 下面是根据各条产生式具体要求生成抽象语法树，涉及细节过多
                if ID == 2:
                    tmpTreeNode.kind = Kind.AllK
                    for s in tmpChildList[0].sibling:
                        tmpTreeNode.sibling.append(s)
                    tmpTreeNode.sibling.append(tmpChildList[1])
                elif ID == 3:
                    tmpTreeNode.kind = Kind.AllK
                    tmpTreeNode.sibling.append(tmpChildList[0])
                elif 6 <= ID <= 7:
                    tmpTreeNode.kind = Kind.VarDefK
                    tmpChildList[0].kind = Kind.TypeNameK
                    tmpTreeNode.children.append(tmpChildList[0])
                    tmpTreeNode.character = tmpChildList[1].character
                    if ID == 7:
                        tmpChildList[3].kind = Kind.NumK
                        tmpTreeNode.children.append(tmpChildList[3])
                elif ID == 10:
                    tmpTreeNode.kind = Kind.FunDefK
                    tmpChildList[0].kind = Kind.TypeNameK
                    tmpChildList[1].kind = Kind.IdK
                    tmpTreeNode.children.append(tmpChildList[0])
                    tmpTreeNode.children.append(tmpChildList[1])
                    tmpTreeNode.children.append(tmpChildList[3])
                    tmpTreeNode.children.append(tmpChildList[5])
                elif 11 <= ID <= 12:
                    tmpTreeNode.kind = Kind.AllParamDefK
                    if ID == 11:
                        for s in tmpChildList[0].sibling:
                            tmpTreeNode.sibling.append(s)
                elif ID == 13:
                    tmpTreeNode.kind = Kind.ParamK
                    for s in tmpChildList[0].sibling:
                        tmpTreeNode.sibling.append(s)
                    tmpTreeNode.sibling.append(tmpChildList[2])
                elif ID == 14:
                    tmpTreeNode.kind = Kind.ParamK
                    tmpTreeNode.sibling.append(tmpChildList[0])
                elif 15 <= ID <= 16:
                    tmpTreeNode.kind = Kind.ParamK
                    tmpChildList[0].kind = Kind.TypeNameK
                    tmpChildList[1].kind = Kind.IdK
                    tmpTreeNode.children.append(tmpChildList[0])
                    tmpTreeNode.children.append(tmpChildList[1])
                    if ID == 16:
                        tmpTreeNode.children.append(nTreeNode(kind=Kind.ParamArrayK))
                elif ID == 17:
                    tmpTreeNode.kind = Kind.CompoundK
                    if tmpChildList[1].kind != Kind.EmptyK:
                        tmpTreeNode.children.append(tmpChildList[1])
                    if tmpChildList[2].kind != Kind.EmptyK:
                        tmpTreeNode.children.append(tmpChildList[2])
                elif ID == 34 or ID == 38 or ID == 46 or ID == 50:
                    if ID == 34:
                        tmpTreeNode.kind = Kind.AssignK
                    else:
                        tmpTreeNode.kind = Kind.OpK
                    tmpTreeNode.character = tmpChildList[1].character
                    tmpTreeNode.children.append(tmpChildList[0])
                    tmpTreeNode.children.append(tmpChildList[2])
                elif ID == 29:
                    tmpTreeNode.kind = Kind.IfK
                    tmpTreeNode.children.append(tmpChildList[2])
                    tmpTreeNode.children.append(tmpChildList[4])
                elif ID == 30:
                    tmpTreeNode.kind = Kind.IfElseK
                    tmpTreeNode.children.append(tmpChildList[2])
                    tmpTreeNode.children.append(tmpChildList[4])
                    tmpTreeNode.children.append(tmpChildList[6])
                elif ID == 31:
                    tmpTreeNode.kind = Kind.WhileK
                    tmpTreeNode.children.append(tmpChildList[2])
                    tmpTreeNode.children.append(tmpChildList[4])
                elif ID == 32:
                    tmpTreeNode.kind = Kind.ReturnK
                    tmpTreeNode.character = tmpChildList[0].character
                elif ID == 33:
                    tmpTreeNode.kind = Kind.ReturnK
                    tmpTreeNode.character = tmpChildList[0].character
                    tmpTreeNode.children.append(tmpChildList[1])
                elif ID == 37:
                    tmpTreeNode.kind = Kind.IdOfArrayK
                    tmpTreeNode.character = tmpChildList[0].character
                    tmpTreeNode.children.append(tmpChildList[2])
                elif 40 <= ID <= 45 or ID == 36 or 48 <= ID <= 49 or 52 <= ID <= 53 or ID == 57:
                    if ID == 36:
                        tmpTreeNode.kind = Kind.IdK
                    elif ID == 57:
                        tmpTreeNode.kind = Kind.NumK
                    else:
                        tmpTreeNode.kind = Kind.OpK
                    tmpTreeNode.character = tmpChildList[0].character
                elif ID == 1 or 4 <= ID <= 5 or 8 <= ID <= 9 or 22 <= ID <= 27 or ID == 35 or ID == 39 or ID == 47 or ID == 51 or 55 <= ID <= 56 or ID == 59:
                    tmpTreeNode = tmpChildList[0]
                elif ID == 20 or ID == 18:
                    if ID == 20:
                        tmpTreeNode.kind = Kind.StK
                    else:
                        tmpTreeNode.kind = Kind.AllVarDefK
                    for s in tmpChildList[0].sibling:
                        if s.kind != Kind.EmptyK:
                            tmpTreeNode.sibling.append(s)
                    if tmpChildList[1].kind != Kind.EmptyK:
                        tmpTreeNode.sibling.append(tmpChildList[1])
                elif ID == 19 or ID == 21 or ID == 28:
                    tmpTreeNode.kind = Kind.EmptyK
                elif ID == 54:
                    tmpTreeNode = tmpChildList[1]
                elif ID == 58:
                    tmpTreeNode.kind = Kind.CallK
                    tmpChildList[0].kind = Kind.FunIDK
                    tmpTreeNode.children.append(tmpChildList[0])
                    tmpTreeNode.children.append(tmpChildList[2])
                elif ID == 60:
                    tmpTreeNode.kind = Kind.ArgsK
                elif ID == 61:
                    tmpTreeNode.kind = Kind.ArgsK
                    for s in tmpChildList[0].sibling:
                        tmpTreeNode.sibling.append(s)
                    tmpTreeNode.sibling.append(tmpChildList[2])
                elif ID == 62:
                    tmpTreeNode.kind = Kind.ArgsK
                    tmpTreeNode.sibling.append(tmpChildList[0])
                else:
                    tmpTreeNode.kind = None
                    tmpTreeNode.character = ReduceExp.symbol
                    tmpTreeNode.children = tmpChildList

                if NowGotoKey in GotoTable:
                    StateStack.push(GotoTable[NowGotoKey])  # 查找goto表是否有符合要求的Key
                    CharacterStack.push(tmpTreeNode)
                else:
                    print("SystemError: Unknown Goto Key: ", NowGotoKey.stateID, NowGotoKey.nonTerminalType)
            # 接受
            else:
                return CharacterStack.top()
    return None

# 生成抽象语法树
def dfs(root: nTreeNode, dep: int):
    if root is None:
        return
    if root.kind != Kind.ArgsK and root.kind != Kind.StK and root.kind != Kind.AllVarDefK and root.kind != Kind.AllParamDefK and root.kind != Kind.AllK:
        if root.kind != Kind.CompoundK:
            print("  " * dep, end="")
        if root.kind == Kind.OpK:
            print("Op: {}".format(root.character.name))
        elif root.kind == Kind.AssignK:
            print("ASSIGN TO: {}".format(root.character.name))
        elif root.kind == Kind.IdK:
            print("ID: {}".format(root.character.name))
        elif root.kind == Kind.NumK:
            print("NUM: {}".format(root.character.name))
        elif root.kind == Kind.ReturnK:
            print("RETURN: ")
        elif root.kind == Kind.IfK or root.kind == Kind.IfElseK:
            print("IF: ")
        elif root.kind == Kind.IdOfArrayK:
            print("ArrayID: {}".format(root.character.name))
        elif root.kind == Kind.VarDefK:
            print("DeFineID: {}".format(root.character.name))
        elif root.kind == Kind.TypeNameK:
            print("TypeName: {}".format(root.character.name))
        elif root.kind == Kind.ParamK:
            print("Pram: ")
        elif root.kind == Kind.ParamArrayK:
            print("ArrayType")
        elif root.kind == Kind.FunIDK:
            print("FUN_ID: {}".format(root.character.name))
        elif root.kind == Kind.FunDefK:
            print("Define FUN_ID: ")
        elif root.kind == Kind.CallK:
            print("CALL")
        elif root.kind == Kind.WhileK:
            print("WHILE")
        elif root.kind == Kind.CompoundK:
            None
        else:
            print(root.character)
        for chl in root.children:
            dfs(chl, dep + 1)
    else:
        for chl in root.sibling:
            dfs(chl, dep)


if __name__ == '__main__':
    TokenList = lexer.lex("r.txt")
    root = LRParse(TokenList)
    if root is None:
        print(False)
    else:
        print(True)
        dfs(root, 0)

        BuildSymTab.BuildSymTable(root)
        for table in BuildSymTab.FunSymTable.values():
            for word in table:
                print(word.type, word.name, word.isarray, word.size)
            print("")
        if not BuildSymTab.ERROR:
            BuildSymTab.CheckType(root)
