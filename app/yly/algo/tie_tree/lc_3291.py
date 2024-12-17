from app.yly.algo.manage import SolutionBase,View
from common.algo.tietree import TieNode
from typing import Dict,List
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    _has_view=True
    uri='https://leetcode.cn/problems/minimum-number-of-valid-strings-to-form-target-i/description/?envType=daily-question&envId=2024-12-17'
    def get_cases(self):
        return [
            dict(words = ["abc","aaaaa","bcdef"], target = "aabcdabc",result=3),
        ]
    
    def get_watch(self):
        return [
            View("root").graph()
        ]

    def init(self, words: List[str], target: str,**kw) -> int:
        self.root=TieNode("",[chr(ord('a')+i) for i in range(26)])
        for w in words:
            self.root.add(w)
        self.target=target
        self.n=len(self.target)
        self.f=[0]*(self.n+1)
    def execute(self):
        self.root.build_fail()
        cur=root=self.root
        for i,c in enumerate(self.target,1):
            cur=cur.childs[c]
            if cur is root:
                return -1
            self.f[i]=self.f[i-cur.depth]+1
        return self.f[self.n]
    def minValidStrings(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()

if __name__=='__main__':
    Solution().run()