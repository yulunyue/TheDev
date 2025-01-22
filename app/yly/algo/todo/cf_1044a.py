from app.yly.algo.manage import SolutionBase,View,np
from typing import Dict,List
from functools import lru_cache
from collections import defaultdict
import bisect
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    uri="https://codeforces.com/problemset/problem/1044/A"
    def get_cases(self):
        return [
            dict(input='''2 3
4
6
1 4 3
1 5 2
1 6 5''',result=2),
        ]
    

        
    def exec(self,**kw):
        n,m=self.il()
        col_x=[]
        row_x=[]
        for _ in range(n):
            x=self.i1()
            col_x.append(x)
        for _ in range(m):
            x1,x2,_=self.il()
            if x1==0:
                row_x.append(x2)
        ans=inf
        col_x.sort()
        row_x.sort()
        l=0
        for i,v in enumerate(col_x):
            while l<len(row_x) and row_x[l]<=v:
                l+=1
            result=len(row_x)-l+1+i+1
            if result<ans:
                ans=result
        return ans
        



if __name__=='__main__':
    Solution().run()