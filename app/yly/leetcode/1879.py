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
            [[100,26,12,62,3,49,55,77,97],[98,0,89,57,34,92,29,75,13],200],
            [[1,2],[2,3],2]
        ]

    def minimumXORSum(self, nums1: List[int], nums2: List[int]) -> int:
        ret=[]
        ans=[dict(),dict()]
        result=0
        for i in range(len(nums1)):
            for j in range(len(nums2)):
                tmp=nums1[i] ^ nums2[j]
                ret.append([tmp-nums1[i],i,j])
        ret.sort()
        for v,i,j in ret:
            if i in ans[0] or j in ans[1]:
                continue
            ans[0][i]=ans[1][j]=1
            result+=v+nums1[i]
        self.log(ret)
        self.log(ans)
        return result



    def test(self,*args):
        return self.minimumXORSum(*args)

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
                print(case,r)
                print(self.logs)
                break
            
    def diff(self,a,b):
        if isinstance(a,float) and isinstance(b,float):
            return "%.2f"%(a)=="%.2f"%(b)
        return a==b

    



      

if __name__ == '__main__':
    Solution().run()



