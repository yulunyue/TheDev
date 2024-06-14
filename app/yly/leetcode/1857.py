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
            ["hhqhuqhqff",[[0,1],[0,2],[2,3],[3,4],[3,5],[5,6],[2,7],[6,7],[7,8],[3,8],[5,8],[8,9],[3,9],[6,9]],3],
            ["a", [[0,0]],-1],
            ["abaca", [[0,1],[0,2],[2,3],[3,4]],3]
        ]
    
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        # colors = [ord(c)-ord('a') for c in colors]
        # self.log(edges,tp="graph")
        g=defaultdict(list)
        # states=[defaultdict(int) for i in range(len(colors))]
        root_ids=[True]*len(colors)
        
        for f,t in edges:
            g[f].append(t)
            root_ids[t]=False
        def has_ring(n,vt:set):
            if n in vt:
                return True
            vt.add(n)
            for v in g[n]:
                if has_ring(v,vt):
                    return True
            vt.remove(n)
            return False
        self.res = -1
        self.state=defaultdict(int)
        @lru_cache(None)
        def dfs(idx):
            if not g[idx]:
                return 1,colors[idx]
            res=-1
            for n in g[idx]:
                v,s=dfs(n)
                res=max(res,v+1 if s==colors[idx] else 0)
            return res

        for i,s in enumerate(root_ids):
            if not s:
                continue
            if has_ring(i,set()):
                return -1
            self.res=max(dfs(i),self.res)
        return self.res

    def check(self,*args):
        pass
    
    def test(self,*args):
        return self.largestPathValue(*args)

    def init(self,*args):
        pass

    def __init__(self,*args) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        self.init(*args)
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
            try:
                r=self.local_debug(*case[:-1])
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r=None
            if not self.diff(r,case[-1]):
                self.check(*case,r)
                print(case,r)
                print(self.logs)
                break
            
    def diff(self,a,b):
        if isinstance(a,float) and isinstance(b,float):
            return "%.2f"%(a)=="%.2f"%(b)
        return a==b

    



      

if __name__ == '__main__':
    Solution().run()



