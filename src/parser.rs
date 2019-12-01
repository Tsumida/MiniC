// 2019-12-1

mod parser\define;

use std::collections::HashMap;
//mod symbol_def;
use symbol_def::SymbolDef::*;

struct PredTable {
    table: HashMap<(Token, String), Vec<String>>,
}