//2019-11-11
use std::cell::{RefCell, Cell};
use std::rc::Rc;

pub type SyntaxTreeNodePtr<T> = Option<Rc<RefCell<SyntaxTreeNode<T>>>>;

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct SyntaxTreeNode<T:Clone + Eq + PartialEq>{
    val: RefCell<T>,
    left: SyntaxTreeNodePtr<T>,
    right: SyntaxTreeNodePtr<T>,
}

impl<T:Clone + Eq + PartialEq> SyntaxTreeNode<T>{
    pub fn new(val:T) -> SyntaxTreeNode<T>{
        SyntaxTreeNode{
            val: RefCell::new(val),
            left: None,
            right: None,
        }
    }

    /// link self.left with node_ptr and return old value.
    fn link_ptr(&mut self, isLeft: bool, node_ptr: SyntaxTreeNodePtr<T>) -> SyntaxTreeNodePtr<T> {
        if isLeft{
            let old_val = match self.left{
                Some(ref rc_node) => Some(rc_node.clone()),
                None => None,
            };
            if let Some(inner) = node_ptr{
                self.left = Some(inner.clone());
            }else{
                self.left = None;
            }
            old_val
        }else{
            let old_val = match self.right{
                Some(ref rc_node) => Some(rc_node.clone()),
                None => None,
            };
            if let Some(inner) = node_ptr{
                self.right = Some(inner.clone());
            }else{
                self.right = None;
            }
            old_val
        }
    }

    fn ptr_link_ptr(isLeft: bool, this: SyntaxTreeNodePtr<T>, other: SyntaxTreeNodePtr<T>)-> SyntaxTreeNodePtr<T> {
        if let Some(ref inner) = this{
            let mut node =  inner.borrow().clone();
            node.link_ptr(isLeft, other)
        }else{
            None
        }
    }

    pub fn link_left_ptr(&mut self, node_ptr: SyntaxTreeNodePtr<T>) -> SyntaxTreeNodePtr<T>{
        self.link_ptr(true, node_ptr)
    } 

    pub fn link_right_ptr(&mut self, node_ptr: SyntaxTreeNodePtr<T>) -> SyntaxTreeNodePtr<T>{
        self.link_ptr(false, node_ptr)
    } 

    pub fn wrap_as_ptr(val: SyntaxTreeNode<T>) -> SyntaxTreeNodePtr<T>{
        Some(Rc::new(RefCell::new(val)))
    }

    pub fn link_left(&mut self, val: T) -> SyntaxTreeNodePtr<T>{
        self.link_ptr(true, 
            SyntaxTreeNode::wrap_as_ptr(SyntaxTreeNode::new(val))
        )
    }

    pub fn link_right(&mut self, val: T) -> SyntaxTreeNodePtr<T>{
        self.link_ptr(false, 
            SyntaxTreeNode::wrap_as_ptr(SyntaxTreeNode::new(val))
        )
    }


    // Immutable reference to ptr
    pub fn get_left_ptr(&self) -> SyntaxTreeNodePtr<T>{
        match self.left{
            None => None,
            Some(ref inner) => Some(inner.clone())
        }
    }

    pub fn get_right_ptr(&self) -> SyntaxTreeNodePtr<T>{
        match self.right{
            None => None,
            Some(ref inner) => Some(inner.clone())
        }
    }

    /// Ptr to Ptr
    pub fn ptr_get_left(node: SyntaxTreeNodePtr<T>) -> SyntaxTreeNodePtr<T>{
        if let Some(ref inner) = node{
            inner.borrow().get_left_ptr()
        }else{
            None
        }
    }
    
    pub fn ptr_get_right(node: SyntaxTreeNodePtr<T>) -> SyntaxTreeNodePtr<T>{
        if let Some(ref inner) = node{
            inner.borrow().get_right_ptr()
        }else{
            None
        }
    }
    
    pub fn get_inorder_vec(node: SyntaxTreeNodePtr<T>, res: &mut Vec<T>){
        if let Some(ref inner) = node{
            SyntaxTreeNode::get_inorder_vec(inner.borrow().get_left_ptr(), res);
            res.push(
                inner.borrow().val.borrow().clone()
            );
            SyntaxTreeNode::get_inorder_vec(inner.borrow().get_right_ptr(), res);
        }
    }

    pub fn get_postorder_vec(node: SyntaxTreeNodePtr<T>, res: &mut Vec<T>){
        if let Some(ref inner) = node{
            SyntaxTreeNode::get_inorder_vec(inner.borrow().get_left_ptr(), res);
            SyntaxTreeNode::get_inorder_vec(inner.borrow().get_right_ptr(), res);
            res.push(
                inner.borrow().val.borrow().clone()
            );
        }
    }

    pub fn merge(val:T, left: SyntaxTreeNodePtr<T>, right: SyntaxTreeNodePtr<T>) -> SyntaxTreeNodePtr<T>{
        //      new_root
        //     /      \
        //  left     right
        Some(Rc::new(RefCell::new(SyntaxTreeNode{
            val:RefCell::new(val),
            left: left,
            right: right,
        })))
    }

}


mod test{
    use super::*;

    fn test_sample_1() -> SyntaxTreeNode<i32>{
        // return old values.
        //          20    
        //        /    \ 
        //     10       30
        let mut root = SyntaxTreeNode::new(20);
        let l = SyntaxTreeNode::new(10);
        let r = SyntaxTreeNode::new(30);
        let _ = root.link_left_ptr(SyntaxTreeNode::wrap_as_ptr(l));
        let _ = root.link_right_ptr(SyntaxTreeNode::wrap_as_ptr(r));

        root
    }

    fn test_sample_2() -> SyntaxTreeNode<i32>{
        // return old values.
        //          20    
        //        /    \ 
        //     10       30
        let mut root = test_sample_1();

        //          50    
        //        /   \ 
        //     70      40
        let mut root2 = SyntaxTreeNode::new(50);
        let l = SyntaxTreeNode::new(70);
        let r = SyntaxTreeNode::new(40);
        let _ = root2.link_left_ptr(SyntaxTreeNode::wrap_as_ptr(l));
        let _ = root2.link_right_ptr(SyntaxTreeNode::wrap_as_ptr(r));

        //                  20    
        //                /   \ 
        //              10     30
        //            /
        //          50    
        //        /   \ 
        //     70      40
        SyntaxTreeNode::ptr_link_ptr(
            true, 
            root.get_left_ptr(), 
            SyntaxTreeNode::wrap_as_ptr(root2.clone())
        );

        root
    }

    #[test]
    fn test_insert() {
        
        let mut root = SyntaxTreeNode::new(20);
        let l = SyntaxTreeNode::new(10);
        let r = SyntaxTreeNode::new(30);
        let res1 = root.link_left_ptr(SyntaxTreeNode::wrap_as_ptr(l));
        let res2 = root.link_right_ptr(SyntaxTreeNode::wrap_as_ptr(r));
       
        assert_eq!(None, res1);
        assert_eq!(None, res2);
 
        assert_eq!(SyntaxTreeNode::wrap_as_ptr(SyntaxTreeNode::new(10)), root.link_left(50));
        assert_eq!(SyntaxTreeNode::wrap_as_ptr(SyntaxTreeNode::new(30)), root.link_right(10))

    }

    #[test]
    fn test_tree_merge() {
        let mut vecs = Vec::new();
        let root = test_sample_2();

        //          20    
        //        /   \ 
        //     10      30
        SyntaxTreeNode::get_inorder_vec(
            SyntaxTreeNode::wrap_as_ptr(root.clone()), 
            &mut vecs
        );
        assert_eq!(
            vec![
                10, 20, 30
            ],
            vecs
        );
        vecs.clear();
        
        let mut root = test_sample_2();
        SyntaxTreeNode::get_inorder_vec(
            SyntaxTreeNode::wrap_as_ptr(root.clone()), 
            &mut vecs
        );
        assert_eq!(
            vec![
                70, 50, 40, 10, 20, 30
            ],
            vecs
        );

    }
}

pub struct SyntaxTree<T:Clone + Eq + PartialEq>{
    root: SyntaxTreeNodePtr<T>,
    num: usize,
}

impl<T:Clone + Eq + PartialEq> SyntaxTree<T>{
    pub fn new() -> SyntaxTree<T>{
        SyntaxTree{
            root: None,
            num: 0usize,
        }
    }

    pub fn merge(new_val: T, left: SyntaxTree<T>, right: SyntaxTree<T>) -> SyntaxTree<T>{
        
        let mut new_tree = SyntaxTree::new();
        if let (Some(left_inner), Some(right_inner)) = (left.root, right.root){
           new_tree.root = Some(
               Rc::new(
                   RefCell::new(
                       SyntaxTreeNode{
                           val: RefCell::new(new_val),
                           left: Some(left_inner),
                           right: Some(right_inner),
                       }
                   )
               )
           )
        }

        new_tree
    }

    pub fn set_num(&mut self, new:usize){
        self.num = new;
    }

    
}
