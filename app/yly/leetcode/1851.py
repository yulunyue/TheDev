from typing import List,Dict,Optional
from collections import defaultdict, deque,Counter
from itertools import accumulate,product
from functools import lru_cache
from sortedcontainers import SortedList
import bisect
import sys
import math
import heapq
inf=float("inf")
null=None
true=True
false=False
M=10**9 + 7

class IntervalTree:
    '''
                    16
        8
    4        12            20
  2   6   10    14     18
 1 3 5 7 9 11 13  15 17  19  21
    '''
    def __init__(self,size,default_value) -> None:
        self.array=[default_value]*size
        self.size=size

    def update_min(self,l,v):
        while l<self.size:
            self.array[l]=v
            l+=l&-l


    def query_min(self,l):
        ret=self.array[l]
        while l>0:
            ret=min(self.array[l],ret)
            l-=l&-l
        return ret
    

class Solution:
    def get_cases(self):
        return [
            [[[9,9],[6,7],[5,6],[2,5],[3,3]],[6,1,1,1,9],[2,-1,-1,-1,1]],
            [[[4,5],[5,8],[1,9],[8,10],[1,6]],[7,9,3,9,3],[4,3,6,3,6]],
            [[[2,3],[2,5],[1,8],[20,25]], [2,19,5,22],[2,-1,4,6]]
        ]
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort(key=lambda v:v[1])
        self.log(intervals)
        n = len(queries)
        ret=[-1]*n
        sl=[]
        queries=sorted([[v,i] for i,v in enumerate(queries)])
        it=IntervalTree(len(intervals),inf)
        while len(queries):
            v,idx=queries.pop()
            while intervals and intervals[-1][-1]>=v:
                p=intervals.pop()
                ai=bisect.bisect_left(sl,p)
                sl.insert(ai,p)
                it.update_min(ai+1,p[1]-p[0]+1)
                # self.log('a',v,ai+1,p[1]-p[0]+1,it.array,sl)
                
            l_max=bisect.bisect_right(sl,[v,0])
            if l_max<len(sl) and sl[l_max][0]==v:
                l_max+=1
            if l_max==0:
                continue
            # res=inf
            # for i in range(l_max):
            #     res=min(res,sl[i][1]-sl[i][0]+1)
            # self.log(v,l_max,res,sl[:l_max])
            # ret[idx]=res
            ret[idx]=it.query_min(l_max) 
            self.log("q",v,it.array,ret[idx],sl)
        return ret
            
            


    def check(self,*args):
        pass
    
    def test(self,*args):
        return self.minInterval(*args)

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
        if tp.startswith('bar'):
            self.draw_bar(s[0],tp)
        self.logs += " ".join([str(v) for v in s])+"\n"
    def draw_bar(self,s,tp):
        from common.tool.draw import Draw
        Draw().draw_bar_chart(s).save(f"data/log/{tp}.png")
    
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



