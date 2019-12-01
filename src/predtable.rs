use std::collections::HashMap;
use std::fs::File;
use std::io::Read;
type PredTable = HashMap<(String, String), Vec<String>>;


fn gen_predtable() -> PredTable{
    vec![
        (("E".to_string(), "id".to_string()), vec!["T".to_string(), "E'".to_string()]),
        (("E".to_string(), "(".to_string()),  vec!["T".to_string(), "E'".to_string()]),

        (("E'".to_string(), "+".to_string()), vec!["+".to_string(), "T".to_string(), "E'".to_string()]),
        (("E'".to_string(), ")".to_string()), vec![]),
        (("E'".to_string(), "$".to_string()), vec![]),

        (("T".to_string(), "id".to_string()), vec!["F".to_string(), "T'".to_string()]),
        (("T".to_string(), "(".to_string()), vec!["F".to_string(), "T'".to_string()]),

        (("T'".to_string(), "+".to_string()), vec![]),
        (("T'".to_string(), "*".to_string()), vec!["*".to_string(), "F".to_string(), "T'".to_string()]),
        (("T'".to_string(), ")".to_string()), vec![]),
        (("T'".to_string(), "$".to_string()), vec![]),

        (("F".to_string(), "id".to_string()), vec!["id".to_string()]),
        (("F".to_string(), "(".to_string()), vec!["(".to_string(), "E".to_string(), ")".to_string()]),
    ].into_iter().collect()
}

fn parse(ts: &Vec<String>){
    let mut stack:Vec<String> = vec!["$".to_string(), "E".to_string()];
    // E是开始符号
    let table: PredTable = gen_predtable();

    let mut x = stack.last().unwrap().clone(); // 必定非空
    let mut index = 0; 
    if ts.len() == 0{
        return;
    }
    let mut step = 0;
    while x != "$"{
        let a = ts.get(index).unwrap().clone();
        step += 1;
        if x == a{
            stack.pop();
            index += 1;
        }else{
            if let Some(item) = table.get(&(x.clone(), a.clone())){
                // 将item顺序压入stack
                stack.pop();
                stack.extend(
                    item.iter().rev().cloned()
                );
                println!("step = {},  {} -> {}", step, x, item.concat());
                println!(" ------------- {}", &stack.concat());
            }else{ // Non-token or error.
                println!("Error: {:?}, {:?}", x, a);
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