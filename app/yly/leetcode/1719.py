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
            dict(pairs =[[1,2],[2,3],[1,3]],result=2),
            dict(pairs =[[3,4],[2,3],[4,5],[2,4],[2,5],[1,5],[1,4]],result=0),
            dict(pairs=[[1,2],[2,3]],result=1),
            
        ]

    def checkWays(self, pairs: List[List[int]]) -> int:
        g=defaultdict(list)
        for x,y in pairs:
            g[x].append(y)
            g[y].append(x)
        keys=sorted(g.keys(),key=lambda v:-len(g[v]))
        for k in keys:
            self.log(k,g[k])
        if len(g[keys[0]])!=len(g.keys())-1:
            return 0
        ans = 1
        for x,y in pairs:
            if len(g[x])==len(g[y]):
                ans = 2
        par=dict()
        for k in keys:
            par[k]=keys[0]
        vis={keys[0]}
        for i in range(1,len(keys)):
            for v in g[keys[i]]:
                if v in vis:
                    continue
                if par[v]!=par[keys[i]]:
                    return 0
                par[v]=keys[i]
            vis.add(keys[i])
        return ans

    def test(self,**kg):
        return self.checkWays(**kg)


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



