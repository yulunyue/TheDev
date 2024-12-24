from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
import bisect
MOD=(10**9)+7
inf = float("inf")
CASE1='''2 4 4
2
1
3'''
RESULT1='''1
2
2'''
CASE2='''4 8 4
4
4
4
4
4
4
4
4'''
RESULT2='''
'''
CASE3='''3 6 3
1
2
1
3
1
3'''
RESULT3='''
'''
class Solution(SolutionBase):
    uri="https://codeforces.com/contest/896/problem/B"
    def get_cases(self):
        return [
            dict(input=CASE3,result=RESULT3),
            dict(input=CASE2,result=RESULT2),
            dict(input=CASE1,result=RESULT1)
        ]
    
    def init(self,**kw):
        self.n,self.m,self.c=self.il()
        self.nums=[]

    def get_watch(self):
        return [
            View("nums").list()
        ]

    def exec1(self):
        self.nums=[]
        for _ in range(self.m):
            v=self.i1()
            if not self.nums or v>=self.nums[-1]:
                self.nums.append(v)
                i=len(self.nums)-1
            else:
                i=bisect.bisect_right(self.nums,v)
                if i<len(self.nums):
                    self.nums[i]=v
            self.log(i,v,self.nums)
            self.output(i+1)
            if len(self.nums)==self.n:
                break

    def exec(self):
        q=0
        self.nums=[0]*(self.n+1)
        while self.m>0:
            self.m-=1
            x=self.i1()
            if x>self.c//2:
                q=self.n
                while self.nums[q]>=x:
                    q-=1
            else:
                q=1
                while self.nums[q] and self.nums[q]<=x:
                    q+=1
            self.log(self.nums, q,x)
            self.output(q)
            self.nums[q]=x
            if all(self.nums[1:]):
                break

if __name__=='__main__':
    Solution().run()