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

class SegTree:
    def __init__(self,size,default_value) -> None:
        self.size=size*4
        self.store=defaultdict(lambda :default_value)
    def update_min_dp(self,o,l,r,v,L,R):
        if l==L and r==R:
            self.store[o]=min(self.store[o],v)
            return self.store[o]
        mid=(L+R)//2
        if r<=mid:
            ret=self.update_min_dp(o*2,l,r,L,mid)
        elif mid<l:
            ret=self.update_min_dp(o*2+1,l,r,mid+1,R)
        else:
            self.update_min_dp(o*2,l,mid,L,mid)
            self.update_min_dp(o*2+1,mid+1,r,mid+1,R)
        return self.store[o]
    
    def update_min(self,l,r,v):
        self.update_min_dp(1,l,r,v,0,self.size)

    def update_sum_dq(self,o,l,r,L,R,v):
        if l==L and r==R:
            self.store[o]+=v
            return 
        mid=(L+R)//2
        if r<=mid:
            self.update_sum_dq(o*2,l,r,L,mid,v)
            self.store[o*2]+=v
        elif mid<l:
            self.update_sum_dq(o*2+1,l,r,mid+1,R,v)
            self.store[o*2+1]+=v
        else:
            self.update_min_dp(o*2,l,mid,L,mid,v)
            self.update_min_dp(o*2+1,mid+1,r,mid+1,R,v)
            self.store[o*2]+=v
            self.store[o*2+1]+=v
    
    def update_sum(self,l,value):
        self.update_sum_dq(1,l,l,0,self.size,value)
   
    def query_sum_dq(self,o,l,r,L,R):
        if l==L and r==R:
            return self.store[o]
        mid=(L+R)//2
        if r<=mid:
            return self.query_sum_dq(o*2,l,r,L,mid)
        elif mid<l:
            return self.query_sum_dq(o*2+1,l,r,mid+1,R)
        return self.query_sum_dq(o*2,l,mid,L,mid)+self.query_sum_dq(o*2+1,mid+1,r,mid+1,R)
            

    def query_sum(self,l,r):
        if r<l:
            return 0
        return self.query_sum_dq(1,l,r,0,self.size)

class Solution:
    def get_cases(self):
        return [
            dict(nums=[3,6,9],queries =[[1,1,1],[1,2,2],[2,2,3]],result=[]),
            dict(nums = [3,1,4,2,5], queries = [[2,3,4],[1,0,4]],result=[0]),
            dict(nums = [4,1,4,2,1,5], queries = [[2,2,4],[1,0,2],[1,0,4]],result=[0,1])
        ]   

    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n=len(nums)
        
        s=SegTree(n,0)
        for i in range(1,n-1):
            if nums[i]>nums[i-1] and nums[i]>nums[i+1]:
                s.update_sum(i,1)
        # nums=[inf]+nums+[inf]
        def util(i,n_state,l_state):
            if n_state and not l_state:
                s.update_sum(i,1)
            if not n_state and l_state:
                s.update_sum(i,-1)
        
        ret = []
        for q,v1,v2 in queries:
            if q==1:
                ret.append(s.query_sum(v1+1,v2-1))
            else:
                util(v1,
                     nums[v1-1]<v2 and v2>nums[v1+1],
                     nums[v1-1]<nums[v1] and nums[v1]>nums[v1+1]
                )
                if v1-2>0:
                    util(v1-1,
                        nums[v1-2]<nums[v1-1] and nums[v1-1]>v2,
                        nums[v1-2]<nums[v1-1] and nums[v1-1]>nums[v1])
                if v1+2<n:
                    util(v1+1,
                        v2<nums[v1+1] and v1+2<n and nums[v1+1]>nums[v1+2],
                        nums[v1]<nums[v1+1] and nums[v1+1]>nums[v1+2])
                nums[v1]=v2
        return ret


    def test(self,**kg):
        return self.countOfPeaks(**kg)


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



