import analyse
import lexer
import parser2
import code_gen

if __name__ == '__main__':
    TokenList = lexer.lex("r.txt")
    root = parser2.LRParse(TokenList)
    if root is None:
        print(False)
    else:
        print(True)
        # parser2.dfs(root, 0)  # 打印抽象语法树
        analyse.semantic_analysis(root)
        # table = analyse.senmantic_analysis(root) 获取三个表
        if not analyse.ERROR:
            code_gen.codegen(root)
