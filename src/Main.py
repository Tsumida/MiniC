import analyse
import lexer
import parser2
import code_gen
'''
Copyright: 
Author: 黄涛
Version: 1.0
Date: 2020-06-11
No history version
充当main，整个代码从这里开始执行
'''
if __name__ == '__main__':
    TokenList = lexer.lex("r.txt") # 词法分析
    root = parser2.LRParse(TokenList) # 语法分析
    if root is None:
        print(False)
    else:
        print(True)
        # parser2.dfs(root, 0)  # 打印抽象语法树
        analyse.semantic_analysis(root) # 语义分析
        # table = analyse.senmantic_analysis(root) 获取三个表
        if not analyse.ERROR:
            code_gen.codegen(root)
