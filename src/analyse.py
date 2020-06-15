from sym_def import Kind
from tree_node import nTreeNode
from symtab_def import *

'''
函数表：
key:函数名
val:函数名，返回值，参数列表
符号表：
key:函数名
val:函数名，里面定义了的各种变量
全局符号表：
全局定义的各种变量
'''

fun_information_table = {}  # 函数表
fun_sym_table = {}  # 所有函数体内的符号表总表s
fun_cnt_size = {}  # 每个函数表里面所有符号需要大小总和
extern_sym_table = []  # 全局变量表
NowList = []  # 当前所在函数体内的符号表,过渡时用

ERROR = False


# 判断列表List中是否有这个name为str的符号
def has_ID(s: str, List):
    for q in List:
        if s == q.name:
            return True
    return False


# 判断列表List中是否有这个name为str的符号，有则返回
def getVal(s: str, List):
    for q in List:
        if s == q.name:
            return q
    return None


# 先把input函数，output函数放进函数表、符号表中
def init():
    q = SymFun_IDNode('input')
    q.type = 'int'
    fun_information_table['input'] = q
    fun_sym_table['input'] = []

    q = SymFun_IDNode('output')
    q.type = 'void'
    param_list = []
    r = SymIDNode(None)
    r.type = 'int'
    r.size = 1
    param_list.append(r)
    q.params = param_list
    fun_information_table['output'] = q
    fun_sym_table['output'] = param_list


# BuildSymTable: #判断函数名和变量名是否重定义、未定义
def build_sym_table(root: nTreeNode, h):
    global fun_sym_table, NowList, fun_information_table, ERROR
    if root.kind != Kind.ArgsK and root.kind != Kind.StK and root.kind != Kind.AllVarDefK and root.kind != Kind.AllParamDefK and root.kind != Kind.AllK:
        if root.kind == Kind.FunDefK:
            p = SymFun_IDNode(root.children[1].character.name)
            p.type = root.children[0].character.name
            param_list = root.children[2].sibling
            for ele in param_list:
                q = SymIDNode(ele.children[1].character.name)
                q.type = ele.children[0].character.name
                if len(ele.children) >= 3:
                    q.isarray = True
                    q.size = 1
                if has_ID(q.name, NowList):
                    print("Redefine params in function <{}> : {}".format(p.name, q.name))  # 函数中参数重名
                    ERROR = True
                p.params.append(q)
                NowList.append(q)
            fun_information_table[p.name] = p
            build_sym_table(root.children[3], h + 1)
            fun_sym_table[p.name] = NowList
            NowList = []
        elif root.kind == Kind.VarDefK:
            q = SymIDNode(root.character.name)
            q.type = root.children[0].character.name
            if len(root.children) >= 2:
                q.isarray = True
                q.size = int(root.children[1].character.name)
            if h == 1:
                if has_ID(q.name, extern_sym_table):
                    print("Redefinition Var: <{}>".format(q.name))  # 全局变量重定义
                    ERROR = True
                extern_sym_table.append(q)
            else:
                if has_ID(q.name, NowList):
                    print("Redefinition Var: <{}>".format(q.name))  # 局部变量重定义
                    ERROR = True
                NowList.append(q)
        elif root.kind == Kind.CallK:
            s = root.children[0].character.name
            if not has_ID(s, fun_information_table.values()):
                print("Undefined Fun_ID: <{}>".format(s))  # 调用函数时该函数名不存在
                ERROR = True
            argslist = root.children[1].sibling
            for ele in argslist:
                build_sym_table(ele, h + 1)
        elif root.kind == Kind.IdK or root.kind == Kind.IdOfArrayK:
            s = root.character.name
            if not has_ID(s, NowList) and not has_ID(s, extern_sym_table):
                print("Undefined Var_ID: <{}>".format(s))  # 变量未定义
                ERROR = True
        else:
            for chl in root.children:
                build_sym_table(chl, h + 1)

    else:
        for chl in root.sibling:
            build_sym_table(chl, h + 1)


now_fun_ID = ''  # 当前所在的函数


# 类型比较器
def CheckType(root: nTreeNode):
    global now_fun_ID, fun_sym_table, fun_information_table, ERROR
    if root.kind != Kind.ArgsK and root.kind != Kind.StK and root.kind != Kind.AllVarDefK and root.kind != Kind.AllParamDefK and root.kind != Kind.AllK:
        if root.kind == Kind.FunDefK:
            now_fun_ID = root.children[1].character.name
            CheckType(root.children[3])
        elif root.kind != Kind.VarDefK:
            for chl in root.children:
                CheckType(chl)
            if root.kind == Kind.NumK:
                root.type = 'int'
                root.val = int(root.character.name)
            elif root.kind == Kind.IdK:
                now_sym_table = fun_sym_table[now_fun_ID]
                q = getVal(root.character.name, now_sym_table)
                if q is None:
                    q = getVal(root.character.name, extern_sym_table)
                root.type = q.type
                root.isarray = q.isarray
            elif root.kind == Kind.IdOfArrayK:
                now_sym_table = fun_sym_table[now_fun_ID]
                q = getVal(root.character.name, now_sym_table)
                if q is None:
                    q = getVal(root.character.name, extern_sym_table)
                if q.type == 'int' and not q.isarray:
                    print('TypeError: var_ID<{}> is an integer type, but it has an index'.format(
                        root.character.name))  # 变量类型错误，被认为是数组
                    ERROR = True
                if not ERROR and root.children[0].type != 'int':
                    print("IndexError: The index of this array isn't an integer")  # 变量类型错误，被认为是int
                    ERROR = True
                root.type = 'int'
            elif root.kind == Kind.ReturnK:
                nowfun = fun_information_table[now_fun_ID]
                if nowfun.type == 'void' and len(root.children) > 0:
                    print("ReturnTypeError: Function <{}> should return void, but return a value".format(
                        now_fun_ID))  # void类型函数返回了一个值
                    ERROR = True
                elif nowfun.type == 'int' and len(root.children) == 0:
                    print("ReturnTypeError: Function <{}> should return a value, but return void".format(
                        now_fun_ID))  # 有返回值函数返回了一个 void
                    ERROR = True
                elif nowfun.type == 'int' and root.children[0].type == 'int' and root.children[0].isarray:
                    print(
                        "ReturnTypeError: Return an array isn't allowed in Function <{}>".format(now_fun_ID))  # 返回了一个数组
                    ERROR = True
            elif root.kind == Kind.CallK:
                args_list = root.children[1].sibling
                param_list = fun_information_table[root.children[0].character.name].params
                if len(args_list) != len(param_list):
                    print("ArgsLengthError: The length of argslist isn't equal to the paramlist")  # 参数长度不一致
                    ERROR = True
                if not ERROR:
                    n = len(args_list)
                    for i in range(n):
                        if args_list[i].type != param_list[i].type or args_list[i].isarray != param_list[i].isarray:
                            print("ArgsTypeError: The {}-th param's type isn't equal to the args".format(i))  # 参数类型不一致
                            ERROR = True
                if not ERROR:
                    root.type = fun_information_table[root.children[0].character.name].type
            elif root.kind == Kind.OpK or root.kind == Kind.AssignK:
                if root.children[0].type != 'int' or root.children[1].type != 'int':
                    print("OperationTypeError: One or two of the side(s) isn't integer")  # 操作符两边的类型不都是int
                    ERROR = True
                if root.children[0].isarray or root.children[1].isarray:
                    print(
                        "OperationTypeError: One or two of the side(s) is array, can't calculate or assign directly")  # 操作符两边的类型不都是int
                    ERROR = True
                if not ERROR:
                    root.type = 'int'
            elif root.kind == Kind.IfK or root.kind == Kind.IfElseK or root.kind == Kind.WhileK:
                if not (root.children[0].type == 'int' and not root.children[0].isarray):
                    print(
                        "ValueError: if, ifElse or while statement needs a integer value to find out where to jump")  # if(else)、while语句判断部分不是int
                    ERROR = True
    else:
        for chl in root.sibling:
            CheckType(chl)


def print_extern_and_fun_sym_table():
    for s in fun_sym_table.keys():
        print("FUN_ID: <{}> return type: <{}>".format(s, fun_information_table[s].type))
        print("type name isarray size offset")
        table = fun_sym_table[s]
        for word in table:
            print(word.type, word.name, word.isarray, word.size, word.offset)
        print("\n\n")
    if len(extern_sym_table) >= 1:
        print("EXTERN:")
        print("type name isarray size offset")
        for word in extern_sym_table:
            print(word.type, word.name, word.isarray, word.size, word.offset)
        print("\n\n")


def semantic_analysis(root: nTreeNode):
    global ERROR
    init()  # 符号表初始化
    build_sym_table(root, 0)  # 建立符号表
    if not ERROR:
        CheckType(root)
    # 每个函数体内符号占用的空间总和：参数无论什么类型都只占1个单位，新定义的变量数组占size个单位,以及各元素的偏移量
    for s in fun_sym_table.keys():
        sum = 0
        tb = fun_sym_table[s]
        for i in range(len(tb)):
            tb[i].offset = sum
            if i < len(fun_information_table[s].params):
                tb[i].size = 1
                sum += 1
            elif tb[i].isarray:
                sum += tb[i].size
            else:
                sum += 1
        fun_cnt_size[s] = sum
    sum = 0
    tb = extern_sym_table
    for i in range(len(tb)):
        tb[i].offset = sum
        if tb[i].isarray:
            sum += tb[i].size
        else:
            tb[i].size = 1
            sum += 1
    fun_cnt_size[s] = sum
    print_extern_and_fun_sym_table()  # 打印符号表
    return SymbolTable(fun_information_table, fun_sym_table, extern_sym_table)
