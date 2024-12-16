from app.yly.algo.manage import SolutionBase
from collections import defaultdict
from common.algo.str_util import z_kmp
import bisect
from typing import Dict,List
import heapq
from functools import lru_cache
import math
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(rooms =[[1,4],[2,3],[3,5],[4,1],[5,2]],queries =[[2,3],[2,4],[2,5]],result=[2,1,3]),
            dict(rooms = [[2,2],[1,2],[3,2]], queries = [[3,1],[3,3],[5,2]],result=[3,-1,3])
        ]

    def init(self, rooms: List[List[int]], queries: List[List[int]]) -> List[int]:
        self.rooms=sorted([[area,idx] for idx,area in rooms])
        self.queries=sorted([[area,idx,i] for i,(idx,area) in enumerate(queries)],reverse=True)

    def execute(self):
        ans= [-1]*len(self.queries)
        rooms=[]
        # self.log(self.rooms)
        # self.log(self.queries)
        for area,idx,i in self.queries:
            while self.rooms and self.rooms[-1][0]>=area:
                _,id2=self.rooms.pop()
                rooms.insert(bisect.bisect_left(rooms,id2),id2)
            if not rooms:
                continue
            
            j=bisect.bisect_left(rooms,idx)
            # self.log(i,j,idx,rooms)
            if j>=len(rooms):
                j-=1
            elif j-1>=0 and abs(rooms[j-1]-idx)<=abs(rooms[j]-idx):
                j-=1
            ans[i]=rooms[j]
        return ans

    
    def closestRoom(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute()

if __name__=='__main__':
    Solution().run()