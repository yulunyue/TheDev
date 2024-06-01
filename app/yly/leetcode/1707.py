from sortedcontainers import SortedList
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
        self.left = left
        self.right = right
class DictTree:
    END='_END'
    def __init__(self) -> None:
        self.map=dict()
    
    def build(self,s1):
        tmp=self.map
        for i,v in enumerate(s1):
            if v not in tmp:
                tmp[v]=dict()
            if i==len(s1)-1:
                tmp[v][self.END]=s1
            tmp=tmp[v]

    def builds(self,s):
        pass

class Solution:
    def get_cases(self):
        return [
            [[5,2,4,6,6,3],[[12,4],[8,1],[6,3]],[15,-1,5]],
            [[0,1,2,3,4], [[3,1],[1,3],[5,6]],[3,3,7]],
            [[536870912,0,534710168,330218644,142254206],[[558240772,1000000000],[307628050,1000000000],[3319300,1000000000],[2751604,683297522],[214004,404207941]],[1050219420,844498962,540190212,539622516,330170208]],


        ]
    
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        nums.sort()
        l_max=nums[-1].bit_length()
        dt=DictTree()
        ZERO='0'
        ONE='1'
        def u(v:int):
            l = v.bit_length() if v else 1
            return ZERO*(l_max-l)+bin(v)[2:]
        for v in nums:
            dt.build(u(v))
        # self.log(dt.map)
        ret=[]
        def query(max_s,qs):
            n=len(qs)
            def dfs(i,is_limit,mp):
                if i>=len(qs):
                    return 0
                if qs[i]==ONE and ZERO in mp:
                    return (1<<(n-i-1))+dfs(i+1, is_limit and max_s[i]==ZERO,mp[ZERO])
                if qs[i]==ZERO and ONE in mp and (not is_limit or max_s[i]==ONE):
                    return (1<<(n-i-1))+dfs(i+1,is_limit,mp[ONE])
                res=0
                if ZERO in mp:
                    res=dfs(i+1,is_limit and max_s[i]==ZERO,mp[ZERO])
                if ONE in mp and (not is_limit or max_s[i]==ONE):
                    res=max(res,dfs(i+1,is_limit,mp[ONE]))
                return res
            ret=dfs(0,True,dt.map)
            self.log(max_s,qs,ret)
            return ret
        for q,m in queries:
            i=bisect.bisect_left(nums,m)
            if nums[0]>m:
                ret.append(-1)
                continue
            elif i>=len(nums):
                max_v=nums[i-1]
            else:
                max_v=nums[i]
            big_sum=0
            if q>max_v:
                v_mask=(1<<max_v.bit_length())-1
                q1=q&v_mask
                big_sum=q-q1
            else:
                q1=q
            ret.append(big_sum+query(u(max_v),u(q1)))
        return ret
    

            

    def check(self,*args):
        pass

    def __init__(self) -> None:
        self.local_debug=getattr(self,sys.argv[-1],None)
        if self.local_debug is None:
            print(sys.argv[-1],"not find")
    logs = ""
    def log(self, *s):
        if not self.local_debug or len(self.logs)>=2048:
            return
        import json
        self.logs += " ".join([json.dumps(v,indent=4) if isinstance(v,dict) else str(v) for v in s])+"\n"
    
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



