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
        

    def exec(self):
        self.n,self.m,self.c=self.il()
        self.nums=[0]*(self.n+1)
        q=0
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
            self.log(self.nums,q,x)
            self.output(q)
            self.nums[q]=x
            if all(self.nums[1:]):
                break

if __name__=='__main__':
    Solution().run()