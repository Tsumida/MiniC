# 2020-06
from enum import Enum
from typing import List

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


# 追加一条注释
def annotation(seq: List[str], msg:str):
    seq.append("* " + msg)


# style: op_code r, d(s)
def rm_code(seq: List[str], num,  op_code:ISA, r:int, d:int, s:int):
    seq.append(f"{num}:    {op_code}  {r},{d}({s})")


# style: op_code r, s, t
def rr_code(seq: List[str], num:int, op_code:ISA, r:int, s:int, t:int):
    seq.append(f"{num}:    {op_code}  {r},{s},{t}")


