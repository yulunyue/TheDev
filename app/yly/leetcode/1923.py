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


class Solution:
    def get_cases(self):
        return [
            dict(n = 5, paths = [[0,1,2,3,4],
                     [2,3,4],
                     [4,0,1,2,3]],result=2)
        ]
    
    def minOperations(self, target: List[int], arr: List[int]) -> int:
        a_m=defaultdict(list)
        for i,a in enumerate(arr):
            a_m[a].append(i)
        q=[]
        ret=0
        bisect.bi
        for w in target:
            if not a_m[w]:
                continue
            while q and q[-1]>a_m[w][0]:
                q.pop()
            q.append(a_m[w][0])
            ret=max(len(q),ret)
            self.log(w,a_m[w],q)
        return len(target)-ret
    def test(self,*args):
        return self.minOperations(*args)
    def check(self,*args):
        pass
    
    def test(self,**kg):
        return self.longestCommonSubpath(**kg)


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



