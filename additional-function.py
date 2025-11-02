#function to find parent

#algorithm
1.start from the root
2.check if the tree is empty, if empty return none
3. Set parent = current node
4.check if parent.key == key then return none because it the root and root has no parent
5. if key < parent.key then go to left child
    5.1. check if key == leftchild.key
    5.2 if true then return parent.key
    5.3 check if key < leftchild.key
    5.4 if true then set parent = current left child
    5.5 go to the left child
    5.6 repeat 
    5.5 else set paretn = current right child

6. else go to the right child 
    6.1 check if key == rightchild.key
    6.2 if true then return parent key
    6.3 check key < rightchild.key
    6.4 if true then set parent = current left child
    6.5 else set parent = current right child 
7.repeat 5 to 6 until key is found or its not found




#psudeo code
parent(self, key)
