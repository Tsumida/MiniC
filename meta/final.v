#############################################################################
#                     U N R E G I S T E R E D   C O P Y
# 
# You are on day 12 of your 30 day trial period.
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
# Date: 04/13/20
# Time: 13:22:45
#
# AYACC Version: 2.07
#############################################################################


##############################################################################
# Rules
##############################################################################

    0  $accept : program $end

    1  program : declaration_list

    2  declaration_list : declaration_list declaration
    3                   | declaration

    4  declaration : var_declaration
    5              | fun_declaration

    6  var_declaration : type_specifier ID SEMI
    7                  | type_specifier ID LBRACKET NUM RBRACKET SEMI

    8  type_specifier : INT
    9                 | VOID

   10  fun_declaration : type_specifier ID LPAREN params RPAREN compound_stmt

   11  params : param_list
   12         | VOID

   13  param_list : param_list COMMA param
   14             | param

   15  param : type_specifier ID
   16        | type_specifier ID LBRACKET RBRACKET

   17  compound_stmt : LBRACE local_declarations statement_list RBRACE

   18  local_declarations : local_declarations var_declaration
   19                     |

   20  statement_list : statement_list statement
   21                 |

   22  statement : expression_stmt
   23            | compound_stmt
   24            | selection_stmt
   25            | iteration_stmt
   26            | return_stmt

   27  expression_stmt : expression SEMI
   28                  | SEMI

   29  selection_stmt : IF LPAREN expression RPAREN statement
   30                 | IF LPAREN expression RPAREN statement ELSE statement

   31  iteration_stmt : WHILE LPAREN expression RPAREN statement

   32  return_stmt : RETURN SEMI
   33              | RETURN expression SEMI

   34  expression : var ASSIGN expression
   35             | simple_expression

   36  var : ID
   37      | ID LBRACKET expression RBRACKET

   38  simple_expression : additive_expression relop additive_expression
   39                    | additive_expression

   40  relop : LT
   41        | LE
   42        | RT
   43        | RE
   44        | EQ
   45        | NEQ

   46  additive_expression : additive_expression addop term
   47                      | term

   48  addop : PLUS
   49        | MINUS

   50  term : term mulop factor
   51       | factor

   52  mulop : TIMES
   53        | OVER

   54  factor : LPAREN expression RPAREN
   55         | var
   56         | call
   57         | NUM

   58  call : ID LPAREN args RPAREN

   59  args : arg_list
   60       |

   61  arg_list : arg_list COMMA expression
   62           | expression


##############################################################################
# States
##############################################################################

state 0
	$accept : . program $end

	INT  shift 1
	VOID  shift 2

	program  goto 3
	declaration_list  goto 4
	declaration  goto 5
	var_declaration  goto 6
	fun_declaration  goto 7
	type_specifier  goto 8


state 1
	type_specifier : INT .  (8)

	.  reduce 8


state 2
	type_specifier : VOID .  (9)

	.  reduce 9


state 3
	$accept : program . $end  (0)

	$end  accept


state 4
	program : declaration_list .  (1)
	declaration_list : declaration_list . declaration

	INT  shift 1
	VOID  shift 2
	.  reduce 1

	declaration  goto 9
	var_declaration  goto 6
	fun_declaration  goto 7
	type_specifier  goto 8


state 5
	declaration_list : declaration .  (3)

	.  reduce 3


state 6
	declaration : var_declaration .  (4)

	.  reduce 4


state 7
	declaration : fun_declaration .  (5)

	.  reduce 5


state 8
	var_declaration : type_specifier . ID SEMI
	var_declaration : type_specifier . ID LBRACKET NUM RBRACKET SEMI
	fun_declaration : type_specifier . ID LPAREN params RPAREN compound_stmt

	ID  shift 10


state 9
	declaration_list : declaration_list declaration .  (2)

	.  reduce 2


state 10
	var_declaration : type_specifier ID . SEMI
	var_declaration : type_specifier ID . LBRACKET NUM RBRACKET SEMI
	fun_declaration : type_specifier ID . LPAREN params RPAREN compound_stmt

	SEMI  shift 11
	LPAREN  shift 12
	LBRACKET  shift 13


state 11
	var_declaration : type_specifier ID SEMI .  (6)

	.  reduce 6


state 12
	fun_declaration : type_specifier ID LPAREN . params RPAREN compound_stmt

	INT  shift 1
	VOID  shift 14

	type_specifier  goto 15
	params  goto 16
	param_list  goto 17
	param  goto 18


state 13
	var_declaration : type_specifier ID LBRACKET . NUM RBRACKET SEMI

	NUM  shift 19


state 14
	type_specifier : VOID .  (9)
	params : VOID .  (12)

	ID  reduce 9
	.  reduce 12


state 15
	param : type_specifier . ID
	param : type_specifier . ID LBRACKET RBRACKET

	ID  shift 20


state 16
	fun_declaration : type_specifier ID LPAREN params . RPAREN compound_stmt

	RPAREN  shift 21


state 17
	params : param_list .  (11)
	param_list : param_list . COMMA param

	COMMA  shift 22
	.  reduce 11


state 18
	param_list : param .  (14)

	.  reduce 14


state 19
	var_declaration : type_specifier ID LBRACKET NUM . RBRACKET SEMI

	RBRACKET  shift 23


state 20
	param : type_specifier ID .  (15)
	param : type_specifier ID . LBRACKET RBRACKET

	LBRACKET  shift 24
	.  reduce 15


state 21
	fun_declaration : type_specifier ID LPAREN params RPAREN . compound_stmt

	LBRACE  shift 25

	compound_stmt  goto 26


state 22
	param_list : param_list COMMA . param

	INT  shift 1
	VOID  shift 2

	type_specifier  goto 15
	param  goto 27


state 23
	var_declaration : type_specifier ID LBRACKET NUM RBRACKET . SEMI

	SEMI  shift 28


state 24
	param : type_specifier ID LBRACKET . RBRACKET

	RBRACKET  shift 29


state 25
	compound_stmt : LBRACE . local_declarations statement_list RBRACE
	local_declarations : .  (19)

	.  reduce 19

	local_declarations  goto 30


state 26
	fun_declaration : type_specifier ID LPAREN params RPAREN compound_stmt .  (10)

	.  reduce 10


state 27
	param_list : param_list COMMA param .  (13)

	.  reduce 13


state 28
	var_declaration : type_specifier ID LBRACKET NUM RBRACKET SEMI .  (7)

	.  reduce 7


state 29
	param : type_specifier ID LBRACKET RBRACKET .  (16)

	.  reduce 16


state 30
	compound_stmt : LBRACE local_declarations . statement_list RBRACE
	local_declarations : local_declarations . var_declaration
	statement_list : .  (21)

	INT  shift 1
	VOID  shift 2
	.  reduce 21

	var_declaration  goto 31
	type_specifier  goto 32
	statement_list  goto 33


state 31
	local_declarations : local_declarations var_declaration .  (18)

	.  reduce 18


state 32
	var_declaration : type_specifier . ID SEMI
	var_declaration : type_specifier . ID LBRACKET NUM RBRACKET SEMI

	ID  shift 34


state 33
	compound_stmt : LBRACE local_declarations statement_list . RBRACE
	statement_list : statement_list . statement

	IF  shift 35
	RETURN  shift 36
	WHILE  shift 37
	SEMI  shift 38
	LPAREN  shift 39
	LBRACE  shift 25
	RBRACE  shift 40
	ID  shift 41
	NUM  shift 42

	compound_stmt  goto 43
	statement  goto 44
	expression_stmt  goto 45
	selection_stmt  goto 46
	iteration_stmt  goto 47
	return_stmt  goto 48
	expression  goto 49
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 34
	var_declaration : type_specifier ID . SEMI
	var_declaration : type_specifier ID . LBRACKET NUM RBRACKET SEMI

	SEMI  shift 11
	LBRACKET  shift 13


state 35
	selection_stmt : IF . LPAREN expression RPAREN statement
	selection_stmt : IF . LPAREN expression RPAREN statement ELSE statement

	LPAREN  shift 56


state 36
	return_stmt : RETURN . SEMI
	return_stmt : RETURN . expression SEMI

	SEMI  shift 57
	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	expression  goto 58
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 37
	iteration_stmt : WHILE . LPAREN expression RPAREN statement

	LPAREN  shift 59


state 38
	expression_stmt : SEMI .  (28)

	.  reduce 28


state 39
	factor : LPAREN . expression RPAREN

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	expression  goto 60
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 40
	compound_stmt : LBRACE local_declarations statement_list RBRACE .  (17)

	.  reduce 17


state 41
	var : ID .  (36)
	var : ID . LBRACKET expression RBRACKET
	call : ID . LPAREN args RPAREN

	LPAREN  shift 61
	LBRACKET  shift 62
	.  reduce 36


state 42
	factor : NUM .  (57)

	.  reduce 57


state 43
	statement : compound_stmt .  (23)

	.  reduce 23


state 44
	statement_list : statement_list statement .  (20)

	.  reduce 20


state 45
	statement : expression_stmt .  (22)

	.  reduce 22


state 46
	statement : selection_stmt .  (24)

	.  reduce 24


state 47
	statement : iteration_stmt .  (25)

	.  reduce 25


state 48
	statement : return_stmt .  (26)

	.  reduce 26


state 49
	expression_stmt : expression . SEMI

	SEMI  shift 63


state 50
	expression : var . ASSIGN expression
	factor : var .  (55)

	ASSIGN  shift 64
	.  reduce 55


state 51
	expression : simple_expression .  (35)

	.  reduce 35


state 52
	simple_expression : additive_expression . relop additive_expression
	simple_expression : additive_expression .  (39)
	additive_expression : additive_expression . addop term

	PLUS  shift 65
	MINUS  shift 66
	LT  shift 67
	LE  shift 68
	RT  shift 69
	RE  shift 70
	EQ  shift 71
	NEQ  shift 72
	.  reduce 39

	relop  goto 73
	addop  goto 74


state 53
	additive_expression : term .  (47)
	term : term . mulop factor

	TIMES  shift 75
	OVER  shift 76
	.  reduce 47

	mulop  goto 77


state 54
	term : factor .  (51)

	.  reduce 51


state 55
	factor : call .  (56)

	.  reduce 56


state 56
	selection_stmt : IF LPAREN . expression RPAREN statement
	selection_stmt : IF LPAREN . expression RPAREN statement ELSE statement

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	expression  goto 78
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 57
	return_stmt : RETURN SEMI .  (32)

	.  reduce 32


state 58
	return_stmt : RETURN expression . SEMI

	SEMI  shift 79


state 59
	iteration_stmt : WHILE LPAREN . expression RPAREN statement

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	expression  goto 80
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 60
	factor : LPAREN expression . RPAREN

	RPAREN  shift 81


state 61
	call : ID LPAREN . args RPAREN
	args : .  (60)

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42
	.  reduce 60

	expression  goto 82
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55
	args  goto 83
	arg_list  goto 84


state 62
	var : ID LBRACKET . expression RBRACKET

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	expression  goto 85
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 63
	expression_stmt : expression SEMI .  (27)

	.  reduce 27


state 64
	expression : var ASSIGN . expression

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	expression  goto 86
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 65
	addop : PLUS .  (48)

	.  reduce 48


state 66
	addop : MINUS .  (49)

	.  reduce 49


state 67
	relop : LT .  (40)

	.  reduce 40


state 68
	relop : LE .  (41)

	.  reduce 41


state 69
	relop : RT .  (42)

	.  reduce 42


state 70
	relop : RE .  (43)

	.  reduce 43


state 71
	relop : EQ .  (44)

	.  reduce 44


state 72
	relop : NEQ .  (45)

	.  reduce 45


state 73
	simple_expression : additive_expression relop . additive_expression

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	var  goto 87
	additive_expression  goto 88
	term  goto 53
	factor  goto 54
	call  goto 55


state 74
	additive_expression : additive_expression addop . term

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	var  goto 87
	term  goto 89
	factor  goto 54
	call  goto 55


state 75
	mulop : TIMES .  (52)

	.  reduce 52


state 76
	mulop : OVER .  (53)

	.  reduce 53


state 77
	term : term mulop . factor

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	var  goto 87
	factor  goto 90
	call  goto 55


state 78
	selection_stmt : IF LPAREN expression . RPAREN statement
	selection_stmt : IF LPAREN expression . RPAREN statement ELSE statement

	RPAREN  shift 91


state 79
	return_stmt : RETURN expression SEMI .  (33)

	.  reduce 33


state 80
	iteration_stmt : WHILE LPAREN expression . RPAREN statement

	RPAREN  shift 92


state 81
	factor : LPAREN expression RPAREN .  (54)

	.  reduce 54


state 82
	arg_list : expression .  (62)

	.  reduce 62


state 83
	call : ID LPAREN args . RPAREN

	RPAREN  shift 93


state 84
	args : arg_list .  (59)
	arg_list : arg_list . COMMA expression

	COMMA  shift 94
	.  reduce 59


state 85
	var : ID LBRACKET expression . RBRACKET

	RBRACKET  shift 95


state 86
	expression : var ASSIGN expression .  (34)

	.  reduce 34


state 87
	factor : var .  (55)

	.  reduce 55


state 88
	simple_expression : additive_expression relop additive_expression .  (38)
	additive_expression : additive_expression . addop term

	PLUS  shift 65
	MINUS  shift 66
	.  reduce 38

	addop  goto 74


state 89
	additive_expression : additive_expression addop term .  (46)
	term : term . mulop factor

	TIMES  shift 75
	OVER  shift 76
	.  reduce 46

	mulop  goto 77


state 90
	term : term mulop factor .  (50)

	.  reduce 50


state 91
	selection_stmt : IF LPAREN expression RPAREN . statement
	selection_stmt : IF LPAREN expression RPAREN . statement ELSE statement

	IF  shift 35
	RETURN  shift 36
	WHILE  shift 37
	SEMI  shift 38
	LPAREN  shift 39
	LBRACE  shift 25
	ID  shift 41
	NUM  shift 42

	compound_stmt  goto 43
	statement  goto 96
	expression_stmt  goto 45
	selection_stmt  goto 46
	iteration_stmt  goto 47
	return_stmt  goto 48
	expression  goto 49
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 92
	iteration_stmt : WHILE LPAREN expression RPAREN . statement

	IF  shift 35
	RETURN  shift 36
	WHILE  shift 37
	SEMI  shift 38
	LPAREN  shift 39
	LBRACE  shift 25
	ID  shift 41
	NUM  shift 42

	compound_stmt  goto 43
	statement  goto 97
	expression_stmt  goto 45
	selection_stmt  goto 46
	iteration_stmt  goto 47
	return_stmt  goto 48
	expression  goto 49
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 93
	call : ID LPAREN args RPAREN .  (58)

	.  reduce 58


state 94
	arg_list : arg_list COMMA . expression

	LPAREN  shift 39
	ID  shift 41
	NUM  shift 42

	expression  goto 98
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 95
	var : ID LBRACKET expression RBRACKET .  (37)

	.  reduce 37


96: shift-reduce conflict (shift 99, reduce 29) on ELSE
state 96
	selection_stmt : IF LPAREN expression RPAREN statement .  (29)
	selection_stmt : IF LPAREN expression RPAREN statement . ELSE statement

	ELSE  shift 99
	.  reduce 29


state 97
	iteration_stmt : WHILE LPAREN expression RPAREN statement .  (31)

	.  reduce 31


state 98
	arg_list : arg_list COMMA expression .  (61)

	.  reduce 61


state 99
	selection_stmt : IF LPAREN expression RPAREN statement ELSE . statement

	IF  shift 35
	RETURN  shift 36
	WHILE  shift 37
	SEMI  shift 38
	LPAREN  shift 39
	LBRACE  shift 25
	ID  shift 41
	NUM  shift 42

	compound_stmt  goto 43
	statement  goto 100
	expression_stmt  goto 45
	selection_stmt  goto 46
	iteration_stmt  goto 47
	return_stmt  goto 48
	expression  goto 49
	var  goto 50
	simple_expression  goto 51
	additive_expression  goto 52
	term  goto 53
	factor  goto 54
	call  goto 55


state 100
	selection_stmt : IF LPAREN expression RPAREN statement ELSE statement .  (30)

	.  reduce 30


##############################################################################
# Summary
##############################################################################

State 96 contains 1 shift-reduce conflict(s)


29 token(s), 30 nonterminal(s)
63 grammar rule(s), 101 state(s)


##############################################################################
# End of File
##############################################################################
