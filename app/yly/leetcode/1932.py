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
class UniFind:
    def __init__(self) -> None:
        self.p=dict()
        self.size=dict()


    def merge(self,f,t):
        f1=self.find(f)
        t1=self.find(t)
        if f1==t1:
            return False
        self.p[f1]=t1
        self.size[t1]+=self.size[f1]
        self.size[f1]=0
        return True
    
    def find(self,v):
        if v not in self.p:
            self.p[v]=v
            self.size[v]=1
        if self.p[v]!=v:
            self.p[v]=self.find(self.p[v])
        return self.p[v]
    
    def update(self):
        for k in self.p:
            self.find(k)

    def get_pkeys(self):
        return set(list(self.p.values()))
    

class Solution:
    def get_cases(self):
        return [
            dict(trees = [[2,1],[3,2,5],[5,4]],result=[3,2,5,1,null,4])
        ]
    def canMerge(self, trees: List[TreeNode]) -> Optional[TreeNode]:
        n = len(trees)
        uf=UniFind()
        res=dict()
        for t in trees:
            res[t.val]=t
            if t.left:
                uf.merge(t.left.val, t.val)
            if t.right:
                uf.merge(t.right.val,t.val)

        s2=set()
        for n in trees:
            a=uf.find(n.val)
            
            s2.add()
        if len(s2)==1:
            return res[list(s2)[0]]
        return None 
        

    
    def test(self,**kg):
        return self.canMerge(**kg)


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



