from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution:
    def get_cases(self):
        return [
            dict(parents =[-1,0,0,2],nums =[5,3,2,1],result=[4,1,3,2]),
            dict(parents = [-1,0,0,2], nums = [1,2,3,4],result=[5,1,1,1]),
        ]
    def smallestMissingValueSubtree(self, parents: List[int], nums: List[int]) -> List[int]:
        g=defaultdict(list)
        for i in range(1,len(parents)):
            g[parents[i]].append(i)
        result=[0]*len(parents)
        def dfs(i,p):
            min_vi=max_vi=nums[i]
            if not g[i]:
                result[i]=1 if nums[i]!=1 else 2
                return result[i],min_vi,max_vi,1
            num=1
            for j in g[i]:
                if j==p:
                    continue
                _,min_vj,max_vj,num1=dfs(j,i)
                min_vi=min(min_vj,min_vi)
                max_vi=max(max_vi,max_vj)
                num+=num1
            if min_vi!=1:
                result[i]=1
            elif max_vi==num:
                result[i]=num+1
            self.log(i,num,min_vi,max_vi)
            return result[i],min_vi,max_vi,num
            

        dfs(0,-1)
        return result

        


    def test(self, **kg):
        return self.smallestMissingValueSubtree(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 2048:
            return
        if tp:
            self.draw(s[0], tp)
        self.logs += " ".join([str(v) for v in s])+"\n"

    def draw(self, s, tp: str):
        from common.tool.draw import Draw
        d = Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")

    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs = ""
            ep = case.pop("result")
            try:
                r = self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, ep):
                print(case, 'result',r, 'except',ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
