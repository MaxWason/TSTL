'''
This (auto-generated) unit test generates an error with the size of the tree being negative. 
Assuming that the property of a non-negatively sized tree is a valid property, then this is a bug.


The way it works is by creating a Node, creating a Tree, and then immediately deleting the node of the (empty) tree. 
There isn't any error handling for this, so it breaks our assumption by making tree.size == -1 and therefore fails the test. 

Picture of the output with the tstl file ran for convenience: http://i.imgur.com/OUilX3l.png

P.S. Thanks for updating tstl on github, the `import sut` errors to generate this file were driving me crazy, but pulling your changes fixed it.
'''

from red_black_tree import *

def check():
    global tree0
    if ("tree0" in globals()): 
        assert tree0.size >= 0


int3 = 7 
check()
bool0 = True 
check()
node3 = Node(int3, bool0) 
check()
tree0 = RedBlackTree() 
check()
tree0.delete(node3)  
check()


print "TEST COMPLETED SUCCESSFULLY"