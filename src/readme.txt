编译原理项目期中汇报

组长：杨慧志， 20172131036
组员：黄涛，20172005016



进度汇报
________________________________________
	代码托管在GitHub，地址为: https://github.com/Tsumida/MiniC
	进度安排见: https://github.com/Tsumida/MiniC/issues/1

	目前已经完成了词法分析、语法分析、语法树生成、语义分析、代码生成。



开发环境：
________________________________________
语言：Python 3.6
IDE： PyCharm
操作系统：Windows10
依赖：
	Qt5.12, 跨平台GUI库，执行源码前必须安装。
	PyQt5, 用于在Python中调用Qt5。



运行:
________________________________________
方式1： python ./MiniC/src/compiler.py （需要事先安装好Qt5.12PyQt5）
方式2: ./minic.exe



GUI界面使用说明:
________________________________________

点击左上角文件 -> Open Source, 选中源文件打开:

点击左上方的确认按钮，进行词法分析并显示结果:

进行了词法分析后，点击右上角的“语法分析按钮”，进行语法分析，以列表形式显示抽象语法树：

点击右下角的“文本形式”按钮可以文本形式显示抽象语法树：

进行语法分析后，点击右上角的“代码生成”，生成TM虚拟代码（文本）：



项目概要说明：
________________________________________
使用Python编写词法分析程序。
利用yacc产生LALR分析表，编写程序解析其输出，编写语法分析器。
语法分析产生抽象语法树后，语义分析器构建符号表。
利用抽象语法树和符号表进行代码生成。
程序采用MVC结构。



源码说明
________________________________________
src/下的文件属于MVC中的Model。src/compiler.py复制MVC中的控制器功能。
    action_table.py: Action表
    analyse.py: 语义分析相关函数
    BNF.py: 产生式集合，用于构建语法树
    BuildSymTab.py: 符号表的构建和操作
    code_gen.py: 代码生成相关
    compiler.py: 主程序、GUI界面入口
    goto_table.py: 存放GOTO表
    lexer.py： 词法分析器
    Main.py: 用于展示语法分析
    parser.py: 语法树相关
    parser2.py: 抽象语法树相关
    parser_demo.py: 用于展示语法分析
    r.txt: 用于展示语法分析的例子
    stack.py: 自定义的stack类

    sym_def.py: 包含各种符号的定义，如Token, NonTerminal
    syntax_analysis.py: 语法分析器
    tree_node.py: 语法树节点、抽象语法树节点
    utils.py： 存放解析YACC输出的函数，用来构建ACTION表和GOTO表


ui, 存放了PyQt5的视图代码。先通过Qt Designer设计界面，导出为.ui文件后，利用PyUIC插件将.ui文件翻译为.py文件，属于MVC结构中的View:
    ui/__init__.py，模块导入代码
    ui/main_body.ui, main_body.py分别是主界面的XML表示和对应的py代码
    ui/text_code.py: 文本化抽象语法树用到的UI代码。


tests/
	测试样例，目前包含两个测试样例:
	test_1.txt: 指导书第1个例子，修改“int x,y;”为“int x; int y;”
	test_sort.txt: 指导书第2个排序的例子,修改“int x,y;”为“int x; int y;”。



