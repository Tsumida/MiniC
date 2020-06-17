from tree_node import nTreeNode
from sym_def import Kind, TokenType
from analyse import fun_information_table, fun_sym_table, fun_cnt_size, extern_sym_table, getVal, has_ID


# 以下这部分都是文件的
def emitComment(s: str):
    print(" * {}".format(s))


emitLoc = 0
highEmitLoc = 0
tmpOffset = 0
pc = 7
mp = 6
gp = 5  # 全局指针
ac = 0
sp = 3  # 栈顶指针
ac1 = 1
ac2 = 2
OUTPUT = []
TraceCode = True


def emitComment(s: str):
    if TraceCode:
        z = "*  {}".format(s)
        print(z)
        OUTPUT.append(z)


def emitRO(op: str, r: int, s: int, t: int, u: str):
    global highEmitLoc, emitLoc
    z = "{}:  {}   {},{},{} ".format(emitLoc, op, r, s, t)
    if TraceCode:
        z = z + u
    print(z)
    OUTPUT.append(z)
    emitLoc = emitLoc + 1
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc


def emitRM(op: str, r: int, d: int, s: int, u: str):
    global highEmitLoc, emitLoc
    z = "{}:  {}   {},{},({}) ".format(emitLoc, op, r, d, s)
    if TraceCode:
        z = z + u
    print(z)
    OUTPUT.append(z)
    emitLoc = emitLoc + 1
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc


def emitSkip(howMany: int):
    global highEmitLoc, emitLoc
    w = emitLoc
    emitLoc += howMany
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc
    return w


def emitBackup(loc: highEmitLoc):
    global highEmitLoc, emitLoc
    if loc > highEmitLoc:
        emitComment("BUG in emitBackup")
    emitLoc = loc


def emitRestore():
    global highEmitLoc, emitLoc
    emitLoc = highEmitLoc


def emitRM_Abs(op: str, r: int, a: int, u: str):
    global highEmitLoc, emitLoc
    z = "{}:  {}   {},{},({}) ".format(emitLoc, op, r, a - (emitLoc + 1), pc, u)
    if TraceCode:
        z = z + u
    print(z)
    OUTPUT.append(z)
    emitLoc = emitLoc + 1
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc


# 以上这部分都是文件的
# 在栈中找出位置
tb = []  # 当前函数体：


def st_lookup(s: str):
    if has_ID(s, tb):  # 先寻找局部变量
        return getVal(s, tb).offset
    else:  # 再寻找全局变量
        return getVal(s, extern_sym_table).offset


# 代码生成

def cgen(root: nTreeNode):
    global tmpOffset, tb
    if root is None:
        return
    savedLoc1, savedLoc2, currentLoc, loc = 0, 0, 0, 0
    if root.kind != Kind.ArgsK and root.kind != Kind.StK and root.kind != Kind.AllVarDefK and root.kind != Kind.AllParamDefK and root.kind != Kind.AllK:
        if root.kind == Kind.FunDefK:
            tb = fun_sym_table[root.children[1].character.name]
        if root.kind == Kind.OpK:
            if TraceCode:
                emitComment('-> Op')
            cgen(root.children[0])
            emitRM('ST', ac, tmpOffset, mp, "op: push left")
            tmpOffset -= 1
            cgen(root.children[1])
            tmpOffset += 1
            emitRM('LD', ac1, tmpOffset, mp, "op: load left")
            NowKind = root.character
            if NowKind.type == TokenType.EQ:
                emitRO("SUB", ac, ac1, ac, "op ==")
                emitRM("JEQ", ac, 2, pc, "br if true")
                emitRM("LDC", ac, 0, ac, "false case")
                emitRM("LDA", pc, 1, pc, "unconditional jmp")
                emitRM("LDC", ac, 1, ac, "true case")
            elif NowKind.type == TokenType.NEQ:
                emitRO("SUB", ac, ac1, ac, "op !=")
                emitRM("JNE", ac, 2, pc, "br if true")
                emitRM("LDC", ac, 0, ac, "false case")
                emitRM("LDA", pc, 1, pc, "unconditional jmp")
                emitRM("LDC", ac, 1, ac, "true case")
            elif NowKind.type == TokenType.LT:
                emitRO("SUB", ac, ac1, ac, "op <")
                emitRM("JLT", ac, 2, pc, "br if true")
                emitRM("LDC", ac, 0, ac, "false case")
                emitRM("LDA", pc, 1, pc, "unconditional jmp")
                emitRM("LDC", ac, 1, ac, "true case")
            elif NowKind.type == TokenType.LE:
                emitRO("SUB", ac, ac1, ac, "op <=")
                emitRM("JLE", ac, 2, pc, "br if true")
                emitRM("LDC", ac, 0, ac, "false case")
                emitRM("LDA", pc, 1, pc, "unconditional jmp")
                emitRM("LDC", ac, 1, ac, "true case")
            elif NowKind.type == TokenType.RT:
                emitRO("SUB", ac, ac1, ac, "op >")
                emitRM("JGT", ac, 2, pc, "br if true")
                emitRM("LDC", ac, 0, ac, "false case")
                emitRM("LDA", pc, 1, pc, "unconditional jmp")
                emitRM("LDC", ac, 1, ac, "true case")
            elif NowKind.type == TokenType.RE:
                emitRO("SUB", ac, ac1, ac, "op >=")
                emitRM("JGE", ac, 2, pc, "br if true")
                emitRM("LDC", ac, 0, ac, "false case")
                emitRM("LDA", pc, 1, pc, "unconditional jmp")
                emitRM("LDC", ac, 1, ac, "true case")
            elif NowKind.type == TokenType.PLUS:
                emitRO("ADD", ac, ac1, ac, "op +")
            elif NowKind.type == TokenType.MINUS:
                emitRO("SUB", ac, ac1, ac, "op -")
            elif NowKind.type == TokenType.TIMES:
                emitRO("MUL", ac, ac1, ac, "op *")
            elif NowKind.type == TokenType.OVER:
                emitRO("DIV", ac, ac1, ac, "op /")
            else:
                emitComment("BUG: Unknown operator")
            if TraceCode:
                emitComment("<- Op")
        elif root.kind == Kind.AssignK:
            cgen(root.children[0])
            emitRO("LD", ac2, ac, gp, 'save the address')
            cgen(root.children[1])
            emitRM("ST", ac, ac2, gp, "store the value")
        elif root.kind == Kind.NumK:
            w = root.character.name
            if TraceCode:
                emitComment('-> Const')
            emitRM('LDC', ac, w, 0, "load const")
            if TraceCode:
                emitComment('<- Const')
        elif root.kind == Kind.ReturnK:
            if len(root.children) >= 1:
                cgen(root.children[0])  # 如果有返回值，那么返回值在ac里面
            emitRO('LDC', ac2, len(tb), gp, 'load the table size')
            emitRO('ADD', sp, ac2, sp, 'move the stack point right')
            emitRM("LDA", pc, 1, pc, "unconditional jmp")
        elif root.kind == Kind.IfK or root.kind == Kind.IfElseK:
            if TraceCode:
                emitComment('-> if')
            cgen(root.children[0])
            savedLoc1 = emitSkip(1)
            emitComment('if: jump to else belongs here')

            cgen(root.children[1])
            savedLoc2 = emitSkip(1)
            emitComment("if: jump to end belongs here")

            currentLoc = emitSkip(0)
            emitBackup(savedLoc1)
            emitRM_Abs("JEQ", ac, currentLoc, "if: jump to else")
            emitRestore()

            if root.kind == Kind.IfElseK:
                cgen(root.children[2])
            currentLoc = emitSkip(0)
            emitBackup(savedLoc2)
            emitRM_Abs('LDA', pc, currentLoc, "jmp to end")
            emitRestore()
            if TraceCode:
                emitComment("<- if")
        elif root.kind == Kind.IdK:
            s = root.character.name
            if TraceCode:
                emitComment("-> Id")
            loc = st_lookup(s)
            emitRM("LD", ac, loc, gp, "load id value")
            if TraceCode:
                emitComment("<- Id")
        elif root.kind == Kind.IdOfArrayK:
            cgen(root.children[0])
            s = root.character.name
            if TraceCode:
                emitComment("-> IdOfArray")
            loc = st_lookup(s)
            emitRM("LD", ac1, loc, gp, "load arrayhead")
            emitRO("ADD", ac, ac1, ac, "Count the absolute address")
            if TraceCode:
                emitComment("<- IdOfArray")
            # elif root.kind == Kind.ParamK:
            a = 3
            # elif root.kind == Kind.ParamArrayK:
            a = 3
            # elif root.kind == Kind.FunIDK:
            a = 3
        elif root.kind == Kind.VarDefK:
            None
        elif root.kind == Kind.CallK:
            s = root.children[0].character.name
            emitRO('LD',ac2,len(fun_sym_table[s]),ac2,'load the call table size')
            emitRO('SUB',sp,ac2,sp,'stack point move to left')
            argslist = root.children[1].sibling
            for i in range(len(argslist)):
                cgen(argslist[i])
                emitRM('LD', ac, sp, i, 'Load the {}-th param'.format(i))
        elif root.kind == Kind.WhileK:
            if TraceCode:
                emitComment('-> repeat')
            savedLoc1 = emitSkip(0)
            emitComment("repeat: jump after body comes back here")
            cgen(root.children[0])
            cgen(root.children[1])
            emitRM_Abs("JEQ", ac, savedLoc1, "repeat: jmp back to body")
            if TraceCode:
                emitComment('<- repeat')
        else:
            for chl in root.children:
                cgen(chl)
    else:
        for chl in root.sibling:
            cgen(chl)


def codegen(root: nTreeNode):
    global tb, st
    emitRO("IN", ac, 0, 0, "read integer value")  # 输入一个数
    emitRM("ST", ac, sp, 0, "read: store value")
    emitRO("OUT", ac, 0, 0, "write ac")  # 输出一个数

    emitRM("LDC", sp, 1024, 0, "stack point is pointed at 1024")
    emitRO('LDC', ac2, len(fun_sym_table['main']), 0, 'Load main table size')
    emitRO('SUB', sp, ac2, sp, 'Change stack point')
    emitRM("LD", mp, 0, ac, "load maxaddress from location 0")
    emitRM("ST", ac, 0, ac, "clear location 0")
    tb = fun_sym_table['main']
    cgen(root)
    emitRO('HALT', 0, 0, 0, '')
