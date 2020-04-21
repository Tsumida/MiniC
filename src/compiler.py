# 2020-04-21
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
    scanning:
        python compiler.py -s --path=./src.txt

    scanning + parsing
        python compiler.py -p --path=./src.txt

    compiling: scanning + parsing + code generating
        python compiler.py -c --path=./src.txt

    :return:
    """

    tks = scanner(path)
    synt = syntax_checker(tks)

main()
