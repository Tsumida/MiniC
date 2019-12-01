// 2019-11-30
/// Tiny c 词法约定
/// 仅允许整数类型，不允许实数类型
/// 标识符由大小写英文字母组成，最多52个。其识别按最长匹配原则
/// 整数后紧跟非数字，或标识符后紧跟非字母认为是一个新Token开始
/// 由{ }括起来符号串都认为是注释部分，该部分在词法分析时被过滤掉
/// 识别出的Token由两个变量：currentToken，tokenString识别，其中currentToken代表Token的类属，为一个名为Terminal的枚举类型，在文件globals.h中定义；tokenString代表Token在程序中出现的形式，即其本来面目。例如整数10的currentToken值为NUM，而tokenString值为‘10’；标识符i的currentToken值为ID，而tokenString值为‘i’
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
            write!(f, "invalid token for Symbol")
        }
    }

    // This is important for other errors to wrap this one.
    impl Error for SymbolError {
        fn description(&self) -> &str {
            "Error in symbol, invalid token"
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
            write!(f, "invalid token")
        }
    }

    // This is important for other errors to wrap this one.
    impl Error for KeywordError {
        fn description(&self) -> &str {
            "invalid token"
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

    #[derive(Debug, Clone, PartialEq, Eq, Hash)]
    pub enum Terminal {
        Keyword(Keyword),
        // include +-*/&^=
        SpecialSymbol(SpecialSymbol),
        // include ,;
        Comment,
        NumberLiteral,
        //StringLiteral(String),
        Identifier,
    }

    impl Display for Terminal{
        fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
            write!(f, "{:?}", self)
        }
    }

    impl FromStr for Terminal{
        type Err = KeywordError;
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
                _ => Err(KeywordError),
            }
        }
    }

    #[derive(Debug, PartialEq, Eq, Hash, Clone)]
    pub enum NonTerminal{
        StmtSeq,
        Stmt,
        IfStmt,
        RepeatStmt,
        WhileStmt,
        DoWhileStmt,
        ForStmt,
        ReadStmt,
        WriteStmt,

        //Assign, // :=
        //AddAssign, // +=

        Exp,
        //CmpOp, // =, <
        //AddOp, // +, -
        //MulOp, // *, /, ^
        SimpleExp, 
        Term, 
        Factor,
    }

}
