from tree_node import nTreeNode
from sym_def import Kind, TokenType

emitLoc = 0
highEmitLoc = 0
tmpOffset = 0
pc = 7
mp = 6
gp = 5
ac = 0
ac1 = 1
OUTPUT = []  # OUTPUT
TraceCode = True

def clean_code_gen():
    OUTPUT.clear()

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


def cgen(root: nTreeNode):
    global tmpOffset
    if root is None:
        return
    savedLoc1, savedLoc2, currentLoc, loc = 0, 0, 0, 0
    if root.kind != Kind.ArgsK and root.kind != Kind.StK and root.kind != Kind.AllVarDefK and root.kind != Kind.AllParamDefK and root.kind != Kind.AllK:
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
            # elif root.kind == Kind.AssignK:
            a = 3
            # elif root.kind == Kind.IdK:
            a = 3
        elif root.kind == Kind.NumK:
            w = root.character.name
            if TraceCode:
                emitComment('-> Const')
            emitRM('LDC', ac, w, 0, "load const")
            if TraceCode:
                emitComment('<- Const')
            # elif root.kind == Kind.ReturnK:
            a = 3
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

            # elif root.kind == Kind.IdOfArrayK:
            a = 3
            # elif root.kind == Kind.ParamK:
            a = 3
            # elif root.kind == Kind.ParamArrayK:
            a = 3
            # elif root.kind == Kind.FunIDK:
            a = 3
            # elif root.kind == Kind.FunDefK:
            a = 3
            # elif root.kind == Kind.CallK:
            a = 3
        elif root.kind == Kind.WhileK:
            if TraceCode:
                emitComment('-> repeat')
            savedLoc1 = emitSkip(0)
            emitComment("repeat: jump after body comes back here")
            cgen(root.children[0])
            cgen(root.children[1])
            emitRM_Abs("JEQ", ac, savedLoc1, "repeat: jmp back to body");
            if TraceCode:
                emitComment('<- repeat')
        else:
            for chl in root.children:
                cgen(chl)
    else:
        for chl in root.sibling:
            cgen(chl)

