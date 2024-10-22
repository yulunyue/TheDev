from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
try:
    from app.yly.leetcode.manage import SolutionBase
except:
    class SolutionBase:
        def log(self, *args, **kwargs):
            pass

        def run(self):
            pass
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7

@lru_cache(None)
def stl_2(n,i):
    '''
    第二类斯特林数
    n个人 放到i个房间, 不允许房间为空
    '''
    if n<i or i==0:
        return 0
    if i==1:
        return 1
    ans=0
    for j in range(1,i):
        ans+=stl_2(n-1,j-1)+j*stl_2(n-1,j)
    return ans

class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(n = 1, x = 2, y = 3,result=6),
            dict(n = 5, x = 2, y = 1,result=32)
        ]
    def execute(self, n: int, x: int, y: int) -> int:
        aij=1
        ans=0
        pow=1
        for i in range(1,min(n,x)+1):
            aij*=(x-i+1)
            pow*=y
            ans=(ans+aij*pow*stl_2(n,i))%M
            # self.log(aij,pow)
        return ans

    def numberOfWays(self, *args, **kg):
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
