from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
from app.yly.algo.manage import SolutionBase,TreeNode




class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(root=[1,2,None,3,4],result=2)
        ]
    def pre(self,root=None,**kwargs):
        kwargs['root']=TreeNode.load_from_lc_array(root)
        return kwargs
    
    def init(self, root: TreeNode, **kwargs):
        self.root:TreeNode = root

    def execute(self) -> int:
        self.res = 0
        self.s=1
        def dfs(c:TreeNode):
            if c is None:
                return 0
            l = dfs(c.left)
            r = dfs(c.right)
            if  c.left and c.right:
                if l==0 and r==0:
                    self.res+=1
                if l==1 and r==1:
                    self.s=0
                else:
                    self.s=1
                return 1
            return l | r
        l=dfs(self.root.left)
        r=dfs(self.root.right)
        return self.res + (0 if l and r else self.s)


    def navigation(self, *args, **kg):
        self.init(*args, **kg)
        return self.execute()


if __name__ == '__main__':
    Solution().run()
