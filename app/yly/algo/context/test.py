

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
MOD = (10**9)+7
try:
    from app.yly.algo.manage import SolutionBase

except:

    class SolutionBase:
        DEV = False

        def log(self, *args, **kwargs):
            pass
        def init(self,*args,**kwagrs):
            pass
        def execute(self, *args, **kwargs):
            pass
        def exec(self):
            pass
        def run(self):
            print(self.exec())

        def watch(self):
            pass


class Solution(SolutionBase):
    uri = "https://leetcode.cn/problems/minimize-the-maximum-adjacent-element-difference/"
    gameid = ''

    def get_cases(self):
        return [
            dict(n = 4, queries = [[0, 3], [0, 2]],result=[1, 1]),
            dict(n =5,queries =[[1,3],[2,4]],result=[3,3]),
        ]
<<<<<<< HEAD


    def init(self, nums: List[int]) -> int:
        self.nums=nums
    
    def execute(self):
        n = len(self.nums)
        min_v,max_v=inf,0

        max_r=0
        while idx<n:
            max_r=max(max_r,self.nums[idx])
            i=idx+1
            while i<n and self.nums[i]==-1:
                i+=1
            if i==idx+2:
                l_append(l2,idx,i)
            elif i>idx+2:
                l_append(l3,idx,i)
            elif i<n and i>0 and self.nums[i-1]!=-1:
                mv=max(mv,abs(self.nums[i]-self.nums[i-1]))
            idx=i

       
=======
     
    def execute(self, n: int, queries: List[List[int]]) -> List[int]:
        dis=list(range(n))
        pre=[[] for _ in range(n)]
        ans=[]
        for a,b in queries:
            pre[b].append(a)
            if dis[a]+1>=dis[b]:
                ans.append(dis[-1])
                continue
            dis[b]=dis[a]+1
            for c in range(b+1,n):
                dis[c]=min(dis[c],dis[c-1]+1)
                for p in pre[c]:
                    dis[c]=min(dis[c],dis[p]+1)
            ans.append(dis[-1])
                
>>>>>>> 3a4de23693d9086a09c4068accf3a376b41e2d05
        return ans


  
        
    def shortestDistanceAfterQueries(self, *arg, **kg):
        self.init(*arg, **kg)
        return self.execute(*arg, **kg)


if __name__ == '__main__':
    Solution().run()
