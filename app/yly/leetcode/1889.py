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
            dict(packages = [2,3,5], boxes = [[4,8],[2,8]], result=6),
            dict(packages = [3,5,8,10,11,12],boxes=[[12],[11,9],[10,5,14]],result=9),
            dict(packages = [2,3,5], boxes = [[1,4],[2,3],[3,4]],result=-1)
            
        ]

    def minWastedSpace(self, packages: List[int], boxes: List[List[int]]) -> int:
        n = len(boxes)
        
        packages.sort()
        ps=[0]+list(accumulate(packages))
        for box in boxes:
            box.sort()
        ret=inf
        for box in boxes:
            i,j=len(box)-1,len(packages)-1
            res = 0
            while box[i]>=packages[j] and i>=0:
                if i==0:
                    j1=0
                else:
                    j1=bisect.bisect_left(packages,box[i-1])
                res+=(j-j1+1)*box[i]-(ps[j+1]-ps[j1])
                i-=1
            if res!=0:
                ret=min(res,ret)
        return ret if ret!=inf else -1



    def test(self,**kg):
        return self.minWastedSpace(**kg)


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



