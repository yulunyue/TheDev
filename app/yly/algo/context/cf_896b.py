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
        self.nums=[]
        for _ in range(self.m):
            v=self.i1()
            i=bisect.bisect_left(self.nums,v)
            if i>=len(self.nums) or self.nums[i]==v:
                self.nums.append(v)
            else:
                self.nums[i]=v
            self.log(i,v,self.nums)
            self.output(i+1)
            if len(self.nums)==self.n:
                break


if __name__=='__main__':
    Solution().run()