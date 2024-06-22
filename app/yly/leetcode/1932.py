from typing import List,Dict,Optional
from collections import defaultdict, deque,Counter
from itertools import accumulate,product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf=float("inf")
null=None
true=True
false=False
M=10**9 + 7
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left:TreeNode = left
        self.right:TreeNode = right

def make_two_search(arr:List[int]):
    root=TreeNode(arr[0])
    for v in arr[1:]:
        insert_seach_node(root,TreeNode(v))
    return root

def insert_seach_node(self:TreeNode,n:TreeNode):
    if n.val<self.val:
        if self.left is None:
            self.left=n
        elif self.left.val==n.val:
            self.left=n
        else:
            insert_seach_node(self.left,n)
    elif n.val>self.val:
        if self.right is None:
            self.right=n
        elif self.right.val==n.val:
            self.right=n
        else:
            insert_seach_node(self.right,n)

def tree_to_array(n:TreeNode):
    ret=[]
    stack=[n]
    while stack:
        c=stack.pop(0)
        if c:
            ret.append(c.val)
            stack.append(c.left)
            stack.append(c.right)
    return ret
    

class Solution:
    def get_cases(self):
        return [
            dict(trees = [[5,3,8],[3,2,6]],result=[]),
            dict(trees = [[2,1],[3,2,5],[5,4]],result=[3,2,5,1,null,4])
        ]
    def canMerge(self, trees: List[TreeNode]) -> Optional[TreeNode]:
        n = len(trees)
        tree_p:dict[str,TreeNode]=dict()
        tree_c:Dict[str,TreeNode]=dict()
        for t in trees:
            tree_p[t.val]=t
            if t.left:
                tree_c[t.left.val]=t
            if t.right:
                tree_c[t.right.val]=t


        root=None
        for n in trees:
            if n.val not in tree_c:
                if root is not None:
                    return
                root=n
                continue
            insert_seach_node(tree_c[n.val],n)

        return root
        

    
    def test(self,trees: List[TreeNode]):
        return tree_to_array(self.canMerge([make_two_search(t) for t in trees]))


    def __init__(self,*args) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        if self.local_debug is None:
            print(sys.argv[-1],"not find")
    logs = ""
    def log(self, *s,tp:str=""):
        if not self.local_debug or len(self.logs)>=2048:
            return
        if tp:
            self.draw(s[0],tp)
        self.logs += " ".join([str(v) for v in s])+"\n"
    def draw(self,s,tp:str):
        from common.tool.draw import Draw
        d=Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")
    
    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs=""
            ep=case.pop("result")
            try:
                r=self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r=None
            if not self.diff(r,ep):
                print(case,r,ep)
                print(self.logs)
                break
            
    def diff(self,a,b):
        if isinstance(a,float) and isinstance(b,float):
            return "%.2f"%(a)=="%.2f"%(b)
        return a==b

    



      

if __name__ == '__main__':
    Solution().run()



