from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product
from sortedcontainers import SortedList
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
            dict(s1 ="l123e",s2 ="44",result=True),
            dict(s1='ab',s2='a2',result=false),
            dict(s1 = "internationalization", s2 = "i18n",result=true),
            dict(s1 = "112s", s2 = "g841",result=true),
            
            
        ]
  
    def possiblyEquals(self, s1: str, s2: str) -> bool:
        def c(s:str):
            if len(s)>2 and s[2].isdigit() and s[1].isdigit() and s[0].isdigit():
                a,b,c=int(s[0]),int(s[1]),int(s[2])
                return [a,a*10+b,a*100+b*10+c]
            if len(s)>1 and s[1].isdigit() and s[0].isdigit():
                a,b=int(s[0]),int(s[1])
                return [a,a*10+b]
            if s[0].isdigit():
                return [int(s[0])]
            return []

        def dfs(s1:str,s2:str):
            if not s2:
                return not s1
            if not s1:
                return False
            a1=c(s1)
            a2=c(s2)
            self.log(s1,a1,'-',s2,a2)
            if not a1 and not a2:
                if s1[0]!=s2[0]:
                    return False
                return dfs(s1[1:],s2[1:])
            if a1 and a2:
                for i,a3 in enumerate(a1):
                    for j,b3 in enumerate(a2):
                        if a3<b3 and dfs(s1[i+1:],s2[j+1:]):
                            return True
                        elif a3>b3 and dfs(s1[i+1:],s2[j+1:]):
                            return True
                        elif dfs(s1[i+1:],s2[j+1:]):
                            return True
                return False
            if a1:
                a1,a2,s1,s2=a2,a1,s2,s1
            l=0
            while l<len(s1) and not s1[l].isdigit():
                l+=1

            for j,v in enumerate(a2):
                if l<v and dfs(s1[l:],s2[j+1:]):
                    return True
            return False
        return dfs(s1,s2)

    def test(self, **kg):
        return self.possiblyEquals(**kg)

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
                print(case, 'result', r, 'except', ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
