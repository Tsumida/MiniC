from unittest import TestCase, skipIf

from src.sym_def import *


class ProcResult:
    def __init__(self, st: int):
        self.state_now = st
        self.action_table = dict()  # K = TokenType, V = int
        self.goto_table = dict()    # K = NonTerminal, V = int
        self.reduce_table = dict()        # . reduce st --> (None, st); ID reduce st --> (TokenType.ID, st)
        self.accept = False

    @staticmethod
    def end_acc(st: int):
        pr = ProcResult(st)
        pr.accept = True
        return pr


def proc_lr_table(text: str):
    """
    从YACC生成的文本中构建LR表。
    :return:
        返回包含ProcResult的列表.
    """
    contents = text.split("state ")[1:]
    results = []
    for cont in contents:
        if cont == "":
            continue
        st_num, parts = cont.split(maxsplit=1)  # 分割出状态号码
        st_num = int(st_num.strip())
        parts = [s.strip() for s in parts.split("\n\n")[1:]]  # 最前面的是产生式, 丢弃
        res = ProcResult(st_num)
        for part in parts:
            parse_part(st_num, part, res)
        results.append(res)

    return results


def parse_part(st_num: int, part: str, res: ProcResult):
    """
    对每一个part都生成一个ProcResult
    :param st_num:
    :param part:
    :return:
    """
    part = part.strip()
    if len(part) == 0:
        return None
    # print("part:\n{}".format(part))
    if part == "$end  accept":
        return  res.end_acc(st_num) # 生成一条接受符号
    if "shift" in part:  # Token shift state
        for line in part.splitlines():
            tk, st = line.strip().split("shift")
            tk = sym_reflect(tk)
            st = int(st)
            res.action_table[tk] = st
    elif "goto" in part:  # NonTerminal goto state
        for line in part.splitlines():
            nt, st = line.strip().split("goto")
            nt = sym_reflect(nt)
            st = int(st)
            res.goto_table[nt] = st
    elif "reduce" in part:  # . reduce state
        line = part.strip()
        tk, st = line.strip().split("reduce")
        tk = sym_reflect(tk)
        st = int(st)
        res.reduce_table[tk] = st
    else:
        raise Exception("Unexpected char in {} for state {}".format(part, st_num))


def sym_reflect(sym: str):
    """
    利用反射从字符串中获得Token或者NonTerminal.
    :param sym:
    :return:
    """
    sym = sym.strip()
    assert len(sym) > 0
    # print("reflect ", sym)
    if sym == ".":
        return None
    c = sym[0]
    if c == "$":
        if sym == "$accpet":
            return TokenType.ACCEPT
        elif sym == "$end":
            return TokenType.EOF
    if c.isupper():  # Token
        return getattr(TokenType, sym)
    if c.islower():  # NonTerminal
        return getattr(NonTerminal, sym)
    return None


DEBUG = 1


class TestUtils(TestCase):
    @skipIf(DEBUG == 0, "debug")
    def test_sym_reflect(self):
        case = [
            ("PLUS", TokenType.PLUS),
            ("LBRACE", TokenType.LBRACE),
        ]

        for k, ans in case:
            oup = sym_reflect(k)
            assert oup == ans, f"Err: expected={ans}, got={oup}"

        try:
            _ = sym_reflect("abcdef")
            assert False, f"Err: Should raise exception"
        except AttributeError:
            pass

    @skipIf(DEBUG == 0, "debug")
    def test_proc_lr_table(self):
        case = """
state 0
    $accept : . program $end
    
    INT  shift 1
    VOID  shift 2
    LBRACE  shift 3

    program  goto 4
    declarationlist  goto 5
    declaration  goto 6
    vardeclaration  goto 7
    fundeclaration  goto 8
    typespecifier  goto 9
    compoundstmt  goto 10


state 1
    typespecifier : INT .  (8)

    .  reduce 8"""
        _ = proc_lr_table(case)

        # 对 lr table 进行测试
        with open("./lr_table.txt", "r") as f:
            text = f.read()
            results = proc_lr_table(text)

            for ele in results:
                print("st={}\n\taction={}\n\tgoto={}\n\treduce={}".format(
                    ele.state_now, ele.action_table, ele.goto_table, ele.reduce_table
                ))

            assert len(results) == 101, f"Err: len={len(results)}"

            # state 42： ID  reduce  9
            oup = results[42].reduce_table.get(TokenType.ID)
            assert oup == 9, f"Err: expected={9}, got={oup}"


