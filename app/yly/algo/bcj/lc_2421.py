from app.yly.algo.manage import SolutionBase,View
from typing import List,Dict
from collections import defaultdict
from common.algo.unifind import UniFind
from common.algo.graph import Graph

M = 10**9 + 7

class Uf(UniFind):
    def init(self):
        self.ways=defaultdict(lambda:1)

    def get_title_key(self):
        return ['ways']
    
    def __str__(self):
        return super().__str__()+str(self.ways)


class Solution(SolutionBase):
    _has_view=True
    _uri='https://leetcode.cn/problems/number-of-good-paths/description/'
    def get_cases(self):
        return [
            dict(vals =[2,5,5,1,5,2,3,5,1,5],edges =[[0,1],[2,1],[3,2],[3,4],[3,5],[5,6],[1,7],[8,4],[9,7]],result=20),
            dict(vals=[1, 3, 2, 1, 3], edges=[
                 [0, 1], [0, 2], [2, 3], [2, 4]], result=6)
        ]
    
 

    def init(self, vals: List[int], edges: List[List[int]],result=0):
        self.ans=result
        self.graph=Graph().load_from_edges(edges).set_values(vals)
        self.uf=Uf(len(vals)).set_values(vals)
        self.result=len(vals)
        self.nums=sorted([[v, i] for i, v in enumerate(vals)])
    
    def get_watch(self):
        return [
            View().add_node(
                View("ans"),
                View("nums"),
                View("result"),
                View("action")
            ),
            View().add_node(
                View("uf",size=10).tree(),
                View("graph",size=10).graph()
            )
        ]
    
    def execute(self,*args,**kw):
        for v, pid in self.nums:
            ppid = self.uf.find(pid)
            for nid,*args in self.graph.g[pid]:
                pnid = self.uf.find(nid)
                if self.graph.values[pnid] > v or pnid == ppid:
                    continue
                self.log(f'merge {pid} {pnid}->{ppid}')
                self.uf.merge(ppid,pnid)
                if self.graph.values[pnid] == v:
                    self.result += self.uf.ways[ppid]*self.uf.ways[pnid]
                    self.uf.ways[ppid]+=self.uf.ways[pnid]
                    
        return self.result

    def numberOfGoodPaths(self, *args, **kg) -> int:
        self.init(*args,**kg)
        return self.execute(*args, **kg)


if __name__ == '__main__':
    Solution().run()
