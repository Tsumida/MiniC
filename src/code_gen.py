# 2020-06
from enum import Enum
from unittest import TestCase, skipIf

REG_PC = 7

INS_ZONE_SIZE = 1024 * 4 * 32       # 128KB
DATA_ZONE_SIZE = 1024 * 32         # 32KB

class ISA(Enum):
    # RR
    HALT = 0
    IN = 1      # reg(r) <- keyboard
    OUT = 2     # reg(r) -> screen
    ADD = 3     # reg(r) = reg(s) op reg(t)
    SUB = 4
    MUL = 5
    DIV = 6

    # RM
    LD = 7      # reg(r) <- mem[d + reg(s)]
    ST = 8      # reg(r) -> mem[d + reg(s)]
    LDA = 9     # reg(r) <- d + reg(s)
    LDC = 10    # reg(r) <- d

    JLT = 11    # <
    JLE = 12    # <=
    JGT = 13    # >
    JGE = 14    # >=
    JEQ = 15    # ==
    JNE = 16    # !=

    def __eq__(self, other):
        return self.name == other.value

    def __str__(self):
        return self.name


class TMCodeGenerator:

    def __init__(self, file_name="code"):
        self.file_name = file_name
        self.output_seq = list()
        self.ins_num = -1

    # 追加一条注释
    def annotation(self, msg: str):
        self.output_seq.append(
            "" + msg
        )

    # def check_rm(self) -> bool: pass

    # def check_rr(self) -> bool: pass

    # style: op_code r, d(s)
    def rm_code(self, op_code: ISA, r:int, d:int, s:int):
        self.ins_num += 1
        self.output_seq.append(
            f"{self.ins_num}    {op_code}  {r},{d}({s})" # 这里，op_code 应该转为字符串
        )

    # style: op_code r, s, t
    def rr_code(self, op_code: ISA, r: int, s:int, t: int):
        self.ins_num += 1
        self.output_seq.append(
            f"{self.ins_num}    {op_code}  {r},{s},{t}" # 这里，op_code 应该转为字符串
        )

    def to_string(self):
        return "\n".join(self.output_seq)

    # 将内容转为.tm文件
    def dump(self):
        pass


DEBUG_TM = 1


class TestTMCode(TestCase):

    @skipIf(DEBUG_TM == 0, "debug")
    def test_rr_code(self):
        gen = TMCodeGenerator()
        gen.rm_code(ISA.LDA, 0, 1, 2)
        ans = "0    LDA  0,1(2)"
        assert ans == gen.to_string()

    @skipIf(DEBUG_TM == 0, "debug")
    def test_rr_code(self):
        gen = TMCodeGenerator()
        gen.rr_code(ISA.ADD, 0, 1, 2)
        ans = "0    ADD  0,1,2"
        assert ans == gen.to_string()
