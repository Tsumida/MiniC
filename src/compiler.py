"""
Author: 杨慧志
该模块是TinyC编译器的入口程序，包含了编译器的完整过程和命令行界面工具。
"""
from typing import List
import sys
import click


from sym_def import Token
from lexer import lex
import syntax_analysis
from syntax_analysis import LRParse


def scanner(src_path: str) -> List[Token]:
    print("scanning source...")
    return lex(src_path)


def syntax_checker(tks: List[Token]):
    print("parsing tokens...")
    try:
        t = LRParse(tks)
        t.dfs_print()
    except syntax_analysis.LRParsingErr as lre:
        print("catch LRParsingErr:\n", lre)
        print("miniC exited.")
        exit(-1)


@click.command()
@click.option("--path", help="path of source.", required=True)
def main(path: str):
    """
    命令行接口， 使用click工具构建
    scanning + parsing
        python ./src/compiler.py -s --path=./tests/test_regular.txt

    :return:
    """

    tks = scanner(path)
    syntax_checker(tks)


main()

