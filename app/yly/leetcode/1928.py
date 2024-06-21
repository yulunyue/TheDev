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
            dict(maxTime = 30, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3],result=11),
            dict(maxTime = 30, edges = [[2,9,14],[1,8,25],[6,10,1],[8,0,4],[0,4,12],[7,11,30],[10,3,26],[9,8,8],[3,10,23],[11,5,19],[4,0,4],[5,4,12],[7,3,19],[10,9,5],[1,10,22],[0,2,6],[9,4,15],[10,5,25],[9,11,10],[9,1,21],[9,6,19],[10,8,28]],passingFees =[24,12,24,30,18,20,18,30,28,10,6,7],result=59)
        ]

    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        g=defaultdict(list)
        n=len(passingFees)
        for a,b,t in edges:
            g[a].append([b,t])
            g[b].append([a,t])
        q=[[passingFees[0],0,0]]
        vt=dict()
        vt[0]=[passingFees[0],0]
        while q:
            use_money,use_time,idx=q.pop(0)
            self.log(use_money,idx,use_time)
            for nid,tm in g[idx]:
                nt=use_time+tm
                nm=use_money+passingFees[nid]
                if use_time+tm>maxTime:
                    continue
                if nid in vt and (vt[nid][0]<=nm and vt[nid][1]<=nt):
                    continue
                if nid in vt:
                    vt[nid]=[min(nm,vt[nid][0]),min(nt,vt[nid][1])]
                else:
                    vt[nid]=[nm,nt]
                q.append([nm,nt]+[nid])
 

        return vt[n-1][0] if n-1 in vt else -1

    
    def test(self,**kg):
        return self.minCost(**kg)


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



