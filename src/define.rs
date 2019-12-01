// 2019-11-30
/// Tiny c 词法约定
/// 仅允许整数类型，不允许实数类型
/// 标识符由大小写英文字母组成，最多52个。其识别按最长匹配原则
/// 整数后紧跟非数字，或标识符后紧跟非字母认为是一个新Terminal开始
/// 由{ }括起来符号串都认为是注释部分，该部分在词法分析时被过滤掉
/// 识别出的Terminal由两个变量：currentTerminal，TerminalString识别，其中currentTerminal代表Terminal的类属，为一个名为Terminal的枚举类型，在文件globals.h中定义；TerminalString代表Terminal在程序中出现的形式，即其本来面目。例如整数10的currentTerminal值为NUM，而TerminalString值为‘10’；标识符i的currentTerminal值为ID，而TerminalString值为‘i’
pub mod SymbolDef{
    use std::error::Error;
    use std::fmt::{self, Display, Formatter};
    use std::iter::Peekable;
    use std::str::Chars;
    use std::str::FromStr;

    #[derive(Debug, Clone, Copy)]
    pub struct SymbolError;

    #[derive(Debug, Clone, PartialEq, Eq, Hash)]
    pub enum SpecialSymbol {
        // Parenthesis `()`
        LeftParenthesis,
        RightParenthesis,
        // Curly Parenthesis `{}`
        LeftBrace,
        RightBrace,
        // ;
        Semicolon,
        // `:=`, "+="
        Assign,
        AddAssign,
        // comparison op, '<', '='
        Smaller,
        Equal,
        // 2^2 = 4, 2^3 = 8
        Power,
        // +, -, *, /
        Add, Minus, Mul, Div
    }

    impl FromStr for SpecialSymbol {
        type Err = SymbolError;

        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s {
                "+" => Ok(SpecialSymbol::Add),
                "-" => Ok(SpecialSymbol::Minus),
                "*" => Ok(SpecialSymbol::Mul),
                "/" => Ok(SpecialSymbol::Div),
                "^" => Ok(SpecialSymbol::Power),
                "=" => Ok(SpecialSymbol::Equal),
                "<" => Ok(SpecialSymbol::Smaller),
                "(" => Ok(SpecialSymbol::LeftParenthesis),
                ")" => Ok(SpecialSymbol::RightParenthesis),
                "{" => Ok(SpecialSymbol::LeftBrace),
                "}" => Ok(SpecialSymbol::RightBrace),
                ":=" => Ok(SpecialSymbol::Assign),
                "+=" => Ok(SpecialSymbol::AddAssign),
                ";" => Ok(SpecialSymbol::Semicolon),
                _ => Err(SymbolError),
            }
        }
    }

    impl Display for SymbolError {
        fn fmt(&self, f: &mut Formatter) -> fmt::Result {
            write!(f, "invalid Terminal for Symbol")
        }
    }

    // This is important for other errors to wrap this one.
    impl Error for SymbolError {
        fn description(&self) -> &str {
            "Error in symbol, invalid Terminal"
        }

        fn cause(&self) -> Option<&dyn Error> {
            // Generic error, underlying cause isn't tracked.
            None
        }
    }

    #[derive(Debug, Clone, Copy)]
    pub struct KeywordError;

    impl Display for KeywordError {
        fn fmt(&self, f: &mut Formatter) -> fmt::Result {
            write!(f, "invalid Terminal")
        }
    }

    // This is important for other errors to wrap this one.
    impl Error for KeywordError {
        fn description(&self) -> &str {
            "invalid Terminal"
        }

        fn cause(&self) -> Option<&dyn Error> {
            // Generic error, underlying cause isn't tracked.
            None
        }
    }

    #[derive(Debug, PartialEq, Eq, Clone, Hash)]
    pub enum Keyword {
        // if
        If,
        Else,
        // repeat .. until ..
        Repeat, Until,
        Do, 
        // while ... do ... endwhile
        While, EndWhile,
        // for ... do ... enddo
        For, EndDo,
    }

    impl FromStr for Keyword {
        type Err = KeywordError;

        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s {
                "if" => Ok(Keyword::If),
                "else" => Ok(Keyword::Else),
                "do" => Ok(Keyword::Do),
                "for" => Ok(Keyword::For),
                "enddo" => Ok(Keyword::EndDo),
                "while" => Ok(Keyword::While),
                "endwhile" => Ok(Keyword::EndWhile),
                "repeat" => Ok(Keyword::Repeat),
                "until" => Ok(Keyword::Until),
                _ => Err(KeywordError),
            }
        }
    }

    #[derive(Debug, Clone, Copy)]
    pub struct TerminalError;

    #[derive(Debug, Clone, PartialEq, Eq, Hash)]
    pub enum Terminal {
        // ------------------------------ Terminal
        Keyword(Keyword),
        // include +-*/&^=
        SpecialSymbol(SpecialSymbol),
        // include ,;
        Comment,
        NumberLiteral,
        //StringLiteral(String),
        Identifier,
        Epsilon, // e
        END, // $

    }

    impl Display for Terminal{
        fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
            write!(f, "{:?}", self)
        }
    }

    impl FromStr for Terminal{
        type Err = TerminalError;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s {
                "if" => Ok(Terminal::Keyword(Keyword::If)),
                "else" => Ok(Terminal::Keyword(Keyword::Else)),
                "do" => Ok(Terminal::Keyword(Keyword::Do)),
                "for" => Ok(Terminal::Keyword(Keyword::For)),
                "enddo" => Ok(Terminal::Keyword(Keyword::EndDo)),
                "while" => Ok(Terminal::Keyword(Keyword::While)),
                "endwhile" => Ok(Terminal::Keyword(Keyword::EndWhile)),
                "repeat" => Ok(Terminal::Keyword(Keyword::Repeat)),
                "until" => Ok(Terminal::Keyword(Keyword::Until)),
                // Special Symbols.
                "+" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Add)),
                "-" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Minus)),
                "*" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Mul)),
                "/" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Div)),
                "^" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Power)),
                "=" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Equal)),
                "<" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Smaller)),
                "(" => Ok(Terminal::SpecialSymbol(SpecialSymbol::LeftParenthesis)),
                ")" => Ok(Terminal::SpecialSymbol(SpecialSymbol::RightParenthesis)),
                "{" => Ok(Terminal::SpecialSymbol(SpecialSymbol::LeftBrace)),
                "}" => Ok(Terminal::SpecialSymbol(SpecialSymbol::RightBrace)),
                ":=" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Assign)),
                "+=" => Ok(Terminal::SpecialSymbol(SpecialSymbol::AddAssign)),
                ";" => Ok(Terminal::SpecialSymbol(SpecialSymbol::Semicolon)),
                // id
                "id" => Ok(Terminal::Identifier),
                _ => Err(TerminalError),
            }
        }
    }

    #[derive(Debug, Clone, PartialEq, Eq, Hash)]
    pub enum NonTerminal {
        // ------------------------------ NonTerminal
        StmtSeq,
        Stmt,
        IfStmt,
        RepeatStmt,
        WhileStmt,
        DoWhileStmt,
        ForStmt,
        ReadStmt,
        WriteStmt,
        Exp,
        SimpleExp, 
        Term, 
        Factor,
    }
    
    #[derive(Debug, Clone, Copy)]
    pub struct NonTerminalError;

    impl Display for NonTerminal{
        fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
            write!(f, "{:?}", self)
        }
    }

    impl FromStr for NonTerminal{
        type Err = NonTerminalError;
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            match s {
                "stmt_sequece" => Ok(NonTerminal::StmtSeq),
                "statement" => Ok(NonTerminal::Stmt),
                "if_stmt" => Ok(NonTerminal::IfStmt),
                "repeat_stmt" => Ok(NonTerminal::RepeatStmt),
                "while_stmt" => Ok(NonTerminal::WhileStmt),
                "dowhile_stmt" => Ok(NonTerminal::DoWhileStmt),
                "for_stmt" => Ok(NonTerminal::ForStmt),
                "read_stmt" => Ok(NonTerminal::ReadStmt),
                "write_stmt" => Ok(NonTerminal:: WriteStmt),
                "exp" => Ok(NonTerminal::Exp),
                "comparison_op" => Ok(NonTerminal::SimpleExp), 
                "simple_exp" => Ok(NonTerminal::Term), 
                "factor" => Ok(NonTerminal::Factor),
                _ => Err(NonTerminalError),
            }
        }
    }



    #[derive(Debug, Clone, PartialEq, Eq, Hash)]
    pub enum Token {
        NonTerminal(NonTerminal),
        Terminal(Terminal),
    }



}
