from sym_def import Kind
from tree_node import nTreeNode
from symtab_def import *


FunInformationTable = {}  # 函数表
FunSymTable = {}  # 所有函数体内的符号表总表s
NowList = []  # 当前所在函数体内的符号表

ERROR = False


def hasID(s: str, List):
    for q in List:
        if s == q.name:
            return True
    return False


def getVal(s: str, List):
    for q in List:
        if s == q.name:
            return q
    return None


# BuildSymTable: #判断函数名和变量名是否重定义、未定义
def BuildSymTable(root: nTreeNode):
    global FunSymTable, NowList, FunInformationTable, ERROR
    if root.kind != Kind.ArgsK and root.kind != Kind.StK and root.kind != Kind.AllVarDefK and root.kind != Kind.AllParamDefK and root.kind != Kind.AllK:
        if root.kind == Kind.FunDefK:
            p = SymFun_IDNode(root.children[1].character.name)
            p.type = root.children[0].character.name
            paramlist = root.children[2].sibling
            for ele in paramlist:
                q = SymIDNode(ele.children[1].character.name)
                q.type = ele.children[0].character.name
                if len(ele.children) >= 3:
                    q.isarray = True
                    q.size = 0x3f3f3f3f
                if hasID(q.name, NowList):
                    print("Redefine params in function <{}> : {}".format(p.name, q.name))
                    ERROR = True
                p.params.append(q)
                NowList.append(q)
            FunInformationTable[p.name] = p
            BuildSymTable(root.children[3])
            FunSymTable[p.name] = NowList
            NowList = []
        elif root.kind == Kind.VarDefK:
            q = SymIDNode(root.character.name)
            q.type = root.children[0].character.name
            if len(root.children) >= 2:
                q.isarray = True
                q.size = int(root.children[1].character.name)
            if hasID(q.name, NowList):
                print("Redefinition Var: <{}>".format(q.name))
                ERROR = True
            NowList.append(q)
        elif root.kind == Kind.CallK:
            s = root.children[0].character.name
            if not hasID(s, FunInformationTable.values()):
                print("Undefined Fun_ID: <{}>".format(s))
                ERROR = True
            argslist = root.children[1].sibling
            for ele in argslist:
                if not hasID(ele.character.name, NowList) and ele.kind != Kind.NumK and ele.kind != Kind.OpK:
                    print("Undefined Var_ID: <{}>".format(ele.character.name))
                    ERROR = True
        elif root.kind == Kind.IdK or root.kind == Kind.IdOfArrayK:
            s = root.character.name
            if not hasID(s, NowList):
                print("Undefined Var_ID: <{}>".format(s))
                ERROR = True
        else:
            for chl in root.children:
                BuildSymTable(chl)

    else:
        for chl in root.sibling:
            BuildSymTable(chl)


nowfunID = ''  # 当前所在的函数


# 类型比较器
def CheckType(root: nTreeNode):
    global nowfunID, FunSymTable, FunInformationTable, ERROR
    if root.kind != Kind.ArgsK and root.kind != Kind.StK and root.kind != Kind.AllVarDefK and root.kind != Kind.AllParamDefK and root.kind != Kind.AllK:
        if root.kind == Kind.FunDefK:
            nowfunID = root.children[1].character.name
            CheckType(root.children[3])
        elif root.kind != Kind.VarDefK:
            for chl in root.children:
                CheckType(chl)
            if root.kind == Kind.NumK:
                root.type = 'int'
            elif root.kind == Kind.IdK:
                nowSymTable = FunSymTable[nowfunID]
                q = getVal(root.character.name, nowSymTable)
                root.type = q.type
                root.isarray = q.isarray
            elif root.kind == Kind.IdOfArrayK:
                nowSymTable = FunSymTable[nowfunID]
                q = getVal(root.character.name,nowSymTable)
                if q.type == 'int' and not q.isarray:
                    print('TypeError: var_ID<{}> is an integer type, but it has an index'.format(root.character.name))
                    ERROR = True
                if not ERROR and root.children[0].type != 'int':
                    print("IndexError: The index of this array isn't an integer")
                    ERROR = True
                root.type = 'int'
            elif root.kind == Kind.ReturnK:
                nowfun = FunInformationTable[nowfunID]
                if nowfun.type == 'void' and len(root.children) > 0:
                    print("ReturnTypeError: Function <{}> should return void, but return a value".format(nowfunID))
                    ERROR = True
                elif nowfun.type == 'int' and len(root.children) == 0:
                    print("ReturnTypeError: Function <{}> should return a value, but return void".format(nowfunID))
                    ERROR = True
                elif nowfun.type == 'int' and root.children[0].type == 'int' and root.children[0].isarray:
                    print("ReturnTypeError: Return an array isn't allowed in Function <{}>".format(nowfunID))
                    ERROR = True
            elif root.kind == Kind.CallK:
                argslist = root.children[1].sibling
                paramlist = FunInformationTable[root.children[0].character.name].params
                if len(argslist) != len(paramlist):
                    print("ArgsLengthError: The length of argslist isn't equal to the paramlist")
                    ERROR = True
                if not ERROR:
                    n = len(argslist)
                    for i in range(n):
                        if argslist[i].type != paramlist[i].type or argslist[i].isarray != paramlist[i].isarray:
                            print("ArgsTypeError: The {}-th param's type isn't equal to the args".format(i))
                            ERROR = True
                if not ERROR:
                    root.type = FunInformationTable[root.children[0].character.name].type
            elif root.kind == Kind.OpK or root.kind == Kind.AssignK:
                if root.children[0].type != 'int' or root.children[1].type != 'int':
                    print("OperationTypeError: One or two of the side(s) isn't integer")
                    ERROR = True
                if root.children[0].isarray or root.children[1].isarray:
                    print("OperationTypeError: One or two of the side(s) is array, can't calculate or assign directly")
                    ERROR = True
                if not ERROR:
                    root.type = 'int'
            elif root.kind == Kind.IfK or root.kind == Kind.IfElseK or root.kind == Kind.WhileK:
                if not(root.children[0].type == 'int' and not root.children[0].isarray):
                    print("ValueError: if, ifElse or while statement needs a integer value to find out where to jump")
    else:
        for chl in root.sibling:
            CheckType(chl)
