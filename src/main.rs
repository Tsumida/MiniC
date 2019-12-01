
//mod syntax_tree;
//use syntax_tree::*;

//use std::collections::HashMap;
use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::Read;

mod define;
use define::SymbolDef::*;
/*
type PreTableItem = Vec<Token>;
type PredTable = HashMap<(Token, Token), PreTableItem>;

fn gen_predtable() -> PredTable{
    vec![
        
    ].into_iter().collect()
}

fn parse(ts: &Vec<Token>){
    let mut stack = vec![Token::END, Token::StmtSeq];
    // E是开始符号
    let table: PredTable = gen_predtable();

    let mut x = stack.last().unwrap().clone(); // 必定非空
    let mut index = 0; 
    if ts.len() == 0{
        return;
    }
    let mut step = 0;
    while x != Token::END{
        let token = ts.get(index).unwrap().clone();
        step += 1;
        if x == token{
            stack.pop();
            index += 1;
        }else{
            if let Some(item) = table.get(&(x.clone(), a.clone())){
                // 将item顺序压入stack
                stack.pop();
                stack.extend(
                    item.iter().rev().cloned()
                );
                //println!("step = {},  {} -> {:?}", step, x, item.concat());
                //println!(" ------------- {:?}", &stack.concat());
            }else{ // Non-token or error.
                println!("Error: {:?}, {:?}", x, token);
                panic!("No such item.");
            }
        }

        if !stack.is_empty(){
            x = stack.last().unwrap().clone();
        }else{
            panic!("Error.");
        }
    }
}
*/

type ProductionSet = HashMap<Token, Vec<Vec<Token>>>;
type FirstSet = HashMap<Token, HashSet<Terminal>>;
fn get_first_set(first_set: &mut FirstSet, production_set: ProductionSet){
   for (token, prod) in production_set.iter(){
        let set = match token{
            Token::Terminal(t) => {
                vec![t.clone()].into_iter().collect()
            },
            Token::NonTerminal(nt) => {
                let mut tmp = HashSet::new();
                let n = prod.len();
                if n > 0{
                    println!("producion set of {:?}: len = {}", token, n);
                    let e = Terminal::Epsilon;
                    let tk_nt = Token::NonTerminal(nt.clone());
                    for row in prod{
                        if let Some(p) = first_set.get(row.get(0).unwrap()){
                            tmp.extend(p.iter().cloned());
                        }
                        let mut is_break = false;
                        for i in 1..n{
                            // X ->Y1Y2Y3...Yn
                            // 当 Epsilon 在 First(Y0)..  First(Yi)时, 将First(Yi+1)的元素加入First(nt)
                            // 只要有一个first集不含epsilon, 终止
                            if let Some(p) = first_set.get(row.get(i-1).unwrap()){
                                if p.contains(&e){
                                    tmp.extend(p.iter().cloned());
                                }else{
                                    is_break = true;
                                }
                            }
                            if is_break{
                                break
                            }
                        }
                    }
                }
                tmp
            },
        };
        first_set.insert(token.clone(), set);
    }
}

#[test]
fn test_get_first_set() {
    // topological sort first.
    let prod_t: ProductionSet = vec![
        (Token::Terminal(Terminal::SpecialSymbol(SpecialSymbol::Add)), vec![]),
        (Token::Terminal(Terminal::Epsilon), vec![]),
        (Token::Terminal(Terminal::SpecialSymbol(SpecialSymbol::Mul)), vec![]),
        (Token::Terminal(Terminal::SpecialSymbol(SpecialSymbol::LeftParenthesis)), vec![]),
        (Token::Terminal(Terminal::Identifier), vec![]),
    ].into_iter().collect();

    let prod_nt: ProductionSet = vec![
        (Token::NonTerminal(NonTerminal::Factor), // F
            vec![
                vec![
                    Token::Terminal(Terminal::SpecialSymbol(SpecialSymbol::LeftParenthesis)),
                    Token::NonTerminal(NonTerminal::Stmt),
                    Token::Terminal(Terminal::SpecialSymbol(SpecialSymbol::RightParenthesis)),

                ],
                vec![
                    Token::Terminal(Terminal::Identifier),
                ],
            ]
        ),
        (Token::NonTerminal(NonTerminal::WriteStmt), // T'
            vec![
                vec![
                    Token::Terminal(Terminal::SpecialSymbol(SpecialSymbol::Mul)),
                    Token::NonTerminal(NonTerminal::Factor),
                    Token::NonTerminal(NonTerminal::WriteStmt),
                ],
                vec![
                    Token::Terminal(Terminal::Epsilon),
                ],
            ]
        ),
        (Token::NonTerminal(NonTerminal::ReadStmt), // T
            vec![
                vec![
                    Token::NonTerminal(NonTerminal::Factor),
                    Token::NonTerminal(NonTerminal::WriteStmt),
                ]
            ]
        ),
        (Token::NonTerminal(NonTerminal::RepeatStmt),  // E'
            vec![
                vec![
                    Token::Terminal(Terminal::SpecialSymbol(SpecialSymbol::Add)),
                    Token::NonTerminal(NonTerminal::ReadStmt),
                    Token::NonTerminal(NonTerminal::RepeatStmt),
                ],
                vec![
                    Token::Terminal(Terminal::Epsilon)
                ]
            ]
        ),
        (Token::NonTerminal(NonTerminal::Stmt), // E
            vec![
                vec![
                    Token::NonTerminal(NonTerminal::ReadStmt),
                    Token::NonTerminal(NonTerminal::RepeatStmt),
                ]
            ] 
        ),
    ].into_iter().collect(); 

    let mut first_set = FirstSet::new();
    // must get first set of terminals.
    get_first_set(&mut first_set, prod_t);
    get_first_set(&mut first_set, prod_nt);

    for (k, v) in first_set.into_iter(){
        println!("{:?}: {:?}", k, v);
    }
}


fn main(){
    //let mut t: SyntaxTree<String> = SyntaxTree::new();
    println!("{}", std::mem::size_of::  <Token>());

}