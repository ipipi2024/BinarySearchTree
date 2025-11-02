Function to find parent given a key and root
parent(self=root, key)

#Algorithm
1. Start from the root node
2. Check if the tree is empty
    2.1. if true then return none
3. Check if root.key == key
    3.1 if true , return none because root cannot have parent
    3.2 if false, set parent = root
    3.3 check if key < parent.key
        3.3.1. if true
            3.3.1.1 check if parent.leftchild == null
                3.3.1.1.1 if true then return none because we have reach end of tree and key has not being found
                3.3.1.1.2 if false , check if key == parent.leftchild.key
                    3.3.1.1.2.1 if true then key is found so return parent.key
                    3.3.1.1.2.2 if false then parent = parent.leftchild
                    3.3.1.1.2.3 repeat 3.3
        3.3.2 if false
            3.3.2.1 check if parent.rightchild == null
                3.3.2.1.1 if true then return none because we have reached end of tree and key has not been found
                3.3.2.1.2 if false, check if key == parent.rightchild.key
                    3.3.2.1.2.1 if true then key is found so return parent.key
                    3.3.2.1.2.2 if false then parent = parent.rightchild
                    3.3.2.1.2.3 repeat 3.3

    