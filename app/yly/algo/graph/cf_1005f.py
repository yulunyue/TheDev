

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
try:
    from app.yly.algo.manage import SolutionBase,View

except:
    class SolutionBase:
        def input(self):
            return input()    
        
        def i1(self):
            return int(self.input())
        
        def il(self):
            return [int(v) for v in self.input().split(' ')]
          
        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass
        
        def init(self,*args,**kwagrs):
            pass
        
        def exec(self,*args,**kwargs):
            pass

        def run(self):
            self.init()
            print(self.exec())

CASE2 = '''
5 6 4
1 2
1 3
2 4
2 5
3 4
3 5
'''
RESULT2='''2
111100
110110'''

CASE1 ='''
4 4 2
1 2 
2 3
1 4
4 3
'''
RESULT1='''2
1110
1011'''


class Solution(SolutionBase):
    _uri = "https://codeforces.com/problemset/problem/1005/F"
    _gameid = 'app.yly.algo.context.cf_1005f'
    game_desc='''
    给定一个图
    '''
    _has_view=True
    def get_cases(self):
        return [
            dict(input=CASE2,result=RESULT2),
                        dict(input='''2 1 200000
2 1''',result='''1
1'''),
            

            dict(input=CASE1,result=RESULT1),
        ]
    
    def init(self,*arg,input=None,result=None,**kwargs):
        self.inp=input
        self.ans=result
        self.root=Graph()
        self.n,self.m,self.k=self.il()
        self.dis = [-1]*self.n
        self.dis[0]=0
        self.q=[0]
        self.edge_mask=[]
        self.pre_edges=[[] for _ in range(self.n)]
        self.out = []
        self.cur = 1
        for i in range(self.m):
            f,t=self.il()
            self.root.add_edge(f-1,t-1,i)
        

    def get_watch2(self):
        return [
            View().add_node(
                View().add_node(
                    View(key='inp',size=2),
                    View(key='ans',size=2),
                ),
                View(key='q'),
                View(key='dis'),
                View(key='pre_edges'),
                View(key='cur'),
                View(key='edge_mask'),
                View(key='out'),
            ),
            View(key='root',size=32).graph()
        ]
    
    def exec(self,*args,**kwagrs):
        while self.q:
            n=len(self.q)
            for _ in range(n):
                u=self.q.pop(0)
                for v,_ in self.root.g[u]:
                    if self.dis[v]==-1:
                        self.dis[v]=self.dis[u]+1
                        self.q.append(v)
        
        for f,t,i in self.root.edges:
            if self.dis[f]==self.dis[t]+1:
                self.pre_edges[f].append(i)
            elif self.dis[t]==self.dis[f]+1:
                self.pre_edges[t].append(i)
        for pre in self.pre_edges:
            if len(pre):
                self.cur*=len(pre)
        self.cur=min(self.cur,self.k)

        for i in range(self.cur):
            self.edge_mask=['0']*self.m
            for j in range(self.n-1,0,-1):
                ln=len(self.pre_edges[j])
                i,k=i//ln,i%ln
                self.edge_mask[self.pre_edges[j][k]]='1'
            self.out.append("".join(self.edge_mask))
        
        return "\n".join([str(self.cur)]+self.out)







if __name__ == '__main__':
    Solution().run()
