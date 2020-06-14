import analyse
import lexer
import parser2

if __name__ == '__main__':
    TokenList = lexer.lex("r.txt")
    root = parser2.LRParse(TokenList)
    if root is None:
        print(False)
    else:
        print(True)
        parser2.dfs(root, 0)  # 打印抽象语法树
        analyse.init()  # 符号表初始化
        analyse.build_sym_table(root, 0)  # 建立符号表
        if not analyse.ERROR:
            analyse.CheckType(root)
        if not analyse.ERROR:
            analyse.need_size()
        analyse.print_extern_and_fun_sym_table()  # 打印符号表
