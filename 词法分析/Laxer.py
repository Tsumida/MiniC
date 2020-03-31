import re
from Global import *


# 去掉注释、空行
def filterResource(oldFileName):
    ncode = ''
    code = ''.join(open(oldFileName, 'r').readlines())
    newCode = re.sub(r"/\*([^\*]|(\*)*[^\*/])*(\*)*\*/", "", code)  # 去掉注释/*     */
    for line in newCode.split('\n'):
        line = line.strip()  # 对每行判断是否空
        line = line.replace('\\t', '')
        line = line.replace('\\n', '')
        if not line:
            continue
        else:
            ncode += line + '\n'
    return ncode


# 扫描每个单词
def scan(code):
    lines = code.split('\n')
    token = []  # 所有代码的token流二元组
    for line in lines:
        word = ''
        line += '\n'
        wordTable = []  # 这一行代码的token流二元组
        i = 0
        while i < len(line):
            #    # if(line[i] not in letters)
            #    #语言中不存在这个字符 抛出错误
            #    continue
            word += line[i]
            if line[i] == ' ' or line[i] in delimiters or line[i] in operator:
                if word[0].isalpha():
                    word = word[:-1]
                    if word in keyWord:
                        # 保留字
                        wordTable.append(Token(word, keyWord[word]))
                    else:
                        # 标识符
                        wordTable.append(Token(word, TokenType.ID))
                elif word[:-1].isdigit():
                    # 是整数
                    wordTable.append(Token(word[:-1], TokenType.NUM))
                if line[i] in delimiters:
                    # 是界符
                    wordTable.append(Token(line[i], delimiters[line[i]]))
                elif line[i] in operator:
                    # 是运算符
                    s = line[i] + line[i + 1]
                    if s in operator:
                        # 贪心匹配占两个字节的运算符
                        wordTable.append(Token(s, operator[s]))
                        i += 1
                    else:
                        # 只占一个字节的运算符
                        wordTable.append(Token(line[i], operator[line[i]]))
                word = ''
            i += 1
        token += wordTable
    token += [Token("$", TokenType.EOF)]  # 整个代码程序的终结符
    return token


def lex(codeFile):
    code = filterResource(codeFile)
    return scan(code)


def main():
    tokenArray = lex("r.txt")
    # 读入代码文件，返回Token列表
    f1 = open('token.txt', 'w')
    for u in tokenArray:
        f1.write("{: <7} {}\n".format(u.name, u.type))
    f1.close()


main()
