#############################################################################
#                     U N R E G I S T E R E D   C O P Y
# 
# You are on day 10 of your 30 day trial period.
# 
# This file was produced by an UNREGISTERED COPY of Parser Generator. It is
# for evaluation purposes only. If you continue to use Parser Generator 30
# days after installation then you are required to purchase a license. For
# more information see the online help or go to the Bumble-Bee Software
# homepage at:
# 
# http://www.bumblebeesoftware.com
# 
# This notice must remain present in the file. It cannot be removed.
#############################################################################

#############################################################################
# myparser.v
# YACC verbose file generated from myparser.y.
# 
# Date: 04/11/20
# Time: 13:08:12
# 
# AYACC Version: 2.07
#############################################################################


##############################################################################
# Rules
##############################################################################

    0  $accept : program $end

    1  program : declarationlist

    2  declarationlist : declarationlist declaration
    3                  | declaration

    4  declaration : vardeclaration
    5              | fundeclaration

    6  vardeclaration : typespecifier ID SEMI
    7                 | typespecifier ID LBRACKET NUM RBRACKET SEMI

    8  typespecifier : INT
    9                | VOID

   10  fundeclaration : typespecifier ID LPAREN params RPAREN
   11                 | compoundstmt

   12  params : paramlist
   13         | VOID

   14  paramlist : paramlist COMMA param
   15            | param

   16  param : typespecifier ID
   17        | typespecifier ID LBRACKET RBRACKET

   18  compoundstmt : LBRACE localdeclarations statementlist RBRACE

   19  localdeclarations : localdeclarations vardeclaration
   20                    |

   21  statementlist : statementlist statement
   22                |

   23  statement : expressionstmt
   24            | compoundstmt
   25            | selectionstmt
   26            | iterationstmt
   27            | returnstmt

   28  expressionstmt : expression SEMI
   29                 | SEMI

   30  selectionstmt : IF LPAREN expression RPAREN statement
   31                | IF LPAREN expression RPAREN statement ELSE statement

   32  iterationstmt : WHILE LPAREN expression RPAREN statement

   33  returnstmt : RETURN SEMI
   34             | RETURN expression SEMI

   35  expression : var ASSIGN expression
   36             | simpleexpression

   37  var : ID
   38      | ID LBRACKET expression RBRACKET

   39  simpleexpression : additiveexpression relop additiveexpression
   40                   | additiveexpression

   41  relop : LT
   42        | LE
   43        | RT
   44        | RE
   45        | EQ
   46        | NEQ

   47  additiveexpression : additiveexpression addop term
   48                     | term

   49  addop : PLUS
   50        | MINUS

   51  term : term mulop factor
   52       | factor

   53  mulop : TIMES
   54        | OVER

   55  factor : LPAREN expression RPAREN
   56         | var
   57         | call
   58         | NUM

   59  call : ID LPAREN args RPAREN

   60  args : arglist
   61       |

   62  arglist : arglist COMMA expression
   63          | expression


##############################################################################
# States
##############################################################################

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

	.  reduce 8


state 2
	typespecifier : VOID .  (9)

	.  reduce 9


state 3
	compoundstmt : LBRACE . localdeclarations statementlist RBRACE
	localdeclarations : .  (20)

	.  reduce 20

	localdeclarations  goto 11


state 4
	$accept : program . $end  (0)

	$end  accept


state 5
	program : declarationlist .  (1)
	declarationlist : declarationlist . declaration

	INT  shift 1
	VOID  shift 2
	LBRACE  shift 3
	.  reduce 1

	declaration  goto 12
	vardeclaration  goto 7
	fundeclaration  goto 8
	typespecifier  goto 9
	compoundstmt  goto 10


state 6
	declarationlist : declaration .  (3)

	.  reduce 3


state 7
	declaration : vardeclaration .  (4)

	.  reduce 4


state 8
	declaration : fundeclaration .  (5)

	.  reduce 5


state 9
	vardeclaration : typespecifier . ID SEMI
	vardeclaration : typespecifier . ID LBRACKET NUM RBRACKET SEMI
	fundeclaration : typespecifier . ID LPAREN params RPAREN

	ID  shift 13


state 10
	fundeclaration : compoundstmt .  (11)

	.  reduce 11


state 11
	compoundstmt : LBRACE localdeclarations . statementlist RBRACE
	localdeclarations : localdeclarations . vardeclaration
	statementlist : .  (22)

	INT  shift 1
	VOID  shift 2
	.  reduce 22

	vardeclaration  goto 14
	typespecifier  goto 15
	statementlist  goto 16


state 12
	declarationlist : declarationlist declaration .  (2)

	.  reduce 2


state 13
	vardeclaration : typespecifier ID . SEMI
	vardeclaration : typespecifier ID . LBRACKET NUM RBRACKET SEMI
	fundeclaration : typespecifier ID . LPAREN params RPAREN

	SEMI  shift 17
	LPAREN  shift 18
	LBRACKET  shift 19


state 14
	localdeclarations : localdeclarations vardeclaration .  (19)

	.  reduce 19


state 15
	vardeclaration : typespecifier . ID SEMI
	vardeclaration : typespecifier . ID LBRACKET NUM RBRACKET SEMI

	ID  shift 20


state 16
	compoundstmt : LBRACE localdeclarations statementlist . RBRACE
	statementlist : statementlist . statement

	IF  shift 21
	RETURN  shift 22
	WHILE  shift 23
	SEMI  shift 24
	LPAREN  shift 25
	LBRACE  shift 3
	RBRACE  shift 26
	ID  shift 27
	NUM  shift 28

	compoundstmt  goto 29
	statement  goto 30
	expressionstmt  goto 31
	selectionstmt  goto 32
	iterationstmt  goto 33
	returnstmt  goto 34
	expression  goto 35
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 17
	vardeclaration : typespecifier ID SEMI .  (6)

	.  reduce 6


state 18
	fundeclaration : typespecifier ID LPAREN . params RPAREN

	INT  shift 1
	VOID  shift 42

	typespecifier  goto 43
	params  goto 44
	paramlist  goto 45
	param  goto 46


state 19
	vardeclaration : typespecifier ID LBRACKET . NUM RBRACKET SEMI

	NUM  shift 47


state 20
	vardeclaration : typespecifier ID . SEMI
	vardeclaration : typespecifier ID . LBRACKET NUM RBRACKET SEMI

	SEMI  shift 17
	LBRACKET  shift 19


state 21
	selectionstmt : IF . LPAREN expression RPAREN statement
	selectionstmt : IF . LPAREN expression RPAREN statement ELSE statement

	LPAREN  shift 48


state 22
	returnstmt : RETURN . SEMI
	returnstmt : RETURN . expression SEMI

	SEMI  shift 49
	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	expression  goto 50
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 23
	iterationstmt : WHILE . LPAREN expression RPAREN statement

	LPAREN  shift 51


state 24
	expressionstmt : SEMI .  (29)

	.  reduce 29


state 25
	factor : LPAREN . expression RPAREN

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	expression  goto 52
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 26
	compoundstmt : LBRACE localdeclarations statementlist RBRACE .  (18)

	.  reduce 18


state 27
	call : ID . LPAREN args RPAREN
	var : ID .  (37)
	var : ID . LBRACKET expression RBRACKET

	LPAREN  shift 53
	LBRACKET  shift 54
	.  reduce 37


state 28
	factor : NUM .  (58)

	.  reduce 58


state 29
	statement : compoundstmt .  (24)

	.  reduce 24


state 30
	statementlist : statementlist statement .  (21)

	.  reduce 21


state 31
	statement : expressionstmt .  (23)

	.  reduce 23


state 32
	statement : selectionstmt .  (25)

	.  reduce 25


state 33
	statement : iterationstmt .  (26)

	.  reduce 26


state 34
	statement : returnstmt .  (27)

	.  reduce 27


state 35
	expressionstmt : expression . SEMI

	SEMI  shift 55


state 36
	factor : var .  (56)
	expression : var . ASSIGN expression

	ASSIGN  shift 56
	.  reduce 56


state 37
	expression : simpleexpression .  (36)

	.  reduce 36


state 38
	simpleexpression : additiveexpression . relop additiveexpression
	simpleexpression : additiveexpression .  (40)
	additiveexpression : additiveexpression . addop term

	PLUS  shift 57
	MINUS  shift 58
	LT  shift 59
	LE  shift 60
	RT  shift 61
	RE  shift 62
	EQ  shift 63
	NEQ  shift 64
	.  reduce 40

	relop  goto 65
	addop  goto 66


state 39
	additiveexpression : term .  (48)
	term : term . mulop factor

	TIMES  shift 67
	OVER  shift 68
	.  reduce 48

	mulop  goto 69


state 40
	term : factor .  (52)

	.  reduce 52


state 41
	factor : call .  (57)

	.  reduce 57


state 42
	typespecifier : VOID .  (9)
	params : VOID .  (13)

	ID  reduce 9
	.  reduce 13


state 43
	param : typespecifier . ID
	param : typespecifier . ID LBRACKET RBRACKET

	ID  shift 70


state 44
	fundeclaration : typespecifier ID LPAREN params . RPAREN

	RPAREN  shift 71


state 45
	params : paramlist .  (12)
	paramlist : paramlist . COMMA param

	COMMA  shift 72
	.  reduce 12


state 46
	paramlist : param .  (15)

	.  reduce 15


state 47
	vardeclaration : typespecifier ID LBRACKET NUM . RBRACKET SEMI

	RBRACKET  shift 73


state 48
	selectionstmt : IF LPAREN . expression RPAREN statement
	selectionstmt : IF LPAREN . expression RPAREN statement ELSE statement

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	expression  goto 74
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 49
	returnstmt : RETURN SEMI .  (33)

	.  reduce 33


state 50
	returnstmt : RETURN expression . SEMI

	SEMI  shift 75


state 51
	iterationstmt : WHILE LPAREN . expression RPAREN statement

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	expression  goto 76
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 52
	factor : LPAREN expression . RPAREN

	RPAREN  shift 77


state 53
	call : ID LPAREN . args RPAREN
	args : .  (61)

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28
	.  reduce 61

	expression  goto 78
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41
	args  goto 79
	arglist  goto 80


state 54
	var : ID LBRACKET . expression RBRACKET

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	expression  goto 81
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 55
	expressionstmt : expression SEMI .  (28)

	.  reduce 28


state 56
	expression : var ASSIGN . expression

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	expression  goto 82
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 57
	addop : PLUS .  (49)

	.  reduce 49


state 58
	addop : MINUS .  (50)

	.  reduce 50


state 59
	relop : LT .  (41)

	.  reduce 41


state 60
	relop : LE .  (42)

	.  reduce 42


state 61
	relop : RT .  (43)

	.  reduce 43


state 62
	relop : RE .  (44)

	.  reduce 44


state 63
	relop : EQ .  (45)

	.  reduce 45


state 64
	relop : NEQ .  (46)

	.  reduce 46


state 65
	simpleexpression : additiveexpression relop . additiveexpression

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	var  goto 83
	additiveexpression  goto 84
	term  goto 39
	factor  goto 40
	call  goto 41


state 66
	additiveexpression : additiveexpression addop . term

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	var  goto 83
	term  goto 85
	factor  goto 40
	call  goto 41


state 67
	mulop : TIMES .  (53)

	.  reduce 53


state 68
	mulop : OVER .  (54)

	.  reduce 54


state 69
	term : term mulop . factor

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	var  goto 83
	factor  goto 86
	call  goto 41


state 70
	param : typespecifier ID .  (16)
	param : typespecifier ID . LBRACKET RBRACKET

	LBRACKET  shift 87
	.  reduce 16


state 71
	fundeclaration : typespecifier ID LPAREN params RPAREN .  (10)

	.  reduce 10


state 72
	paramlist : paramlist COMMA . param

	INT  shift 1
	VOID  shift 2

	typespecifier  goto 43
	param  goto 88


state 73
	vardeclaration : typespecifier ID LBRACKET NUM RBRACKET . SEMI

	SEMI  shift 89


state 74
	selectionstmt : IF LPAREN expression . RPAREN statement
	selectionstmt : IF LPAREN expression . RPAREN statement ELSE statement

	RPAREN  shift 90


state 75
	returnstmt : RETURN expression SEMI .  (34)

	.  reduce 34


state 76
	iterationstmt : WHILE LPAREN expression . RPAREN statement

	RPAREN  shift 91


state 77
	factor : LPAREN expression RPAREN .  (55)

	.  reduce 55


state 78
	arglist : expression .  (63)

	.  reduce 63


state 79
	call : ID LPAREN args . RPAREN

	RPAREN  shift 92


state 80
	args : arglist .  (60)
	arglist : arglist . COMMA expression

	COMMA  shift 93
	.  reduce 60


state 81
	var : ID LBRACKET expression . RBRACKET

	RBRACKET  shift 94


state 82
	expression : var ASSIGN expression .  (35)

	.  reduce 35


state 83
	factor : var .  (56)

	.  reduce 56


state 84
	simpleexpression : additiveexpression relop additiveexpression .  (39)
	additiveexpression : additiveexpression . addop term

	PLUS  shift 57
	MINUS  shift 58
	.  reduce 39

	addop  goto 66


state 85
	additiveexpression : additiveexpression addop term .  (47)
	term : term . mulop factor

	TIMES  shift 67
	OVER  shift 68
	.  reduce 47

	mulop  goto 69


state 86
	term : term mulop factor .  (51)

	.  reduce 51


state 87
	param : typespecifier ID LBRACKET . RBRACKET

	RBRACKET  shift 95


state 88
	paramlist : paramlist COMMA param .  (14)

	.  reduce 14


state 89
	vardeclaration : typespecifier ID LBRACKET NUM RBRACKET SEMI .  (7)

	.  reduce 7


state 90
	selectionstmt : IF LPAREN expression RPAREN . statement
	selectionstmt : IF LPAREN expression RPAREN . statement ELSE statement

	IF  shift 21
	RETURN  shift 22
	WHILE  shift 23
	SEMI  shift 24
	LPAREN  shift 25
	LBRACE  shift 3
	ID  shift 27
	NUM  shift 28

	compoundstmt  goto 29
	statement  goto 96
	expressionstmt  goto 31
	selectionstmt  goto 32
	iterationstmt  goto 33
	returnstmt  goto 34
	expression  goto 35
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 91
	iterationstmt : WHILE LPAREN expression RPAREN . statement

	IF  shift 21
	RETURN  shift 22
	WHILE  shift 23
	SEMI  shift 24
	LPAREN  shift 25
	LBRACE  shift 3
	ID  shift 27
	NUM  shift 28

	compoundstmt  goto 29
	statement  goto 97
	expressionstmt  goto 31
	selectionstmt  goto 32
	iterationstmt  goto 33
	returnstmt  goto 34
	expression  goto 35
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 92
	call : ID LPAREN args RPAREN .  (59)

	.  reduce 59


state 93
	arglist : arglist COMMA . expression

	LPAREN  shift 25
	ID  shift 27
	NUM  shift 28

	expression  goto 98
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 94
	var : ID LBRACKET expression RBRACKET .  (38)

	.  reduce 38


state 95
    param : typespecifier ID LBRACKET RBRACKET .  (17)

	.  reduce 17


96: shift-reduce conflict (shift 99, reduce 30) on ELSE
state 96
	selectionstmt : IF LPAREN expression RPAREN statement .  (30)
	selectionstmt : IF LPAREN expression RPAREN statement . ELSE statement

	ELSE  shift 99
	.  reduce 30


state 97
	iterationstmt : WHILE LPAREN expression RPAREN statement .  (32)

	.  reduce 32


state 98
	arglist : arglist COMMA expression .  (62)

	.  reduce 62


state 99
	selectionstmt : IF LPAREN expression RPAREN statement ELSE . statement

	IF  shift 21
	RETURN  shift 22
	WHILE  shift 23
	SEMI  shift 24
	LPAREN  shift 25
	LBRACE  shift 3
	ID  shift 27
	NUM  shift 28

	compoundstmt  goto 29
	statement  goto 100
	expressionstmt  goto 31
	selectionstmt  goto 32
	iterationstmt  goto 33
	returnstmt  goto 34
	expression  goto 35
	var  goto 36
	simpleexpression  goto 37
	additiveexpression  goto 38
	term  goto 39
	factor  goto 40
	call  goto 41


state 100
	selectionstmt : IF LPAREN expression RPAREN statement ELSE statement .  (31)

	.  reduce 31


##############################################################################
# Summary
##############################################################################

State 96 contains 1 shift-reduce conflict(s)


29 token(s), 30 nonterminal(s)
64 grammar rule(s), 101 state(s)


##############################################################################
# End of File
##############################################################################
