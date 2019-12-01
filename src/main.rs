
//mod syntax_tree;
//use syntax_tree::*;

//use std::collections::HashMap;

mod define;
use define::SymbolDef::*;




fn main(){
    //let mut t: SyntaxTree<String> = SyntaxTree::new();
    println!("{}", std::mem::size_of::<NonTerminal>());
    println!("{}", std::mem::size_of::  <Terminal>());

}