

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq




try:
    from app.yly.algo.manage import SolutionBase,div,bp,divh,divv,tree

except:
    class SolutionBase:
        def i1(self):
            return int(sys.stdin.readline().strip())
        
        def il(self,n):
            return [[int(v) for v in sys.stdin.readline().strip().split(' ')] for _ in range(n)]
        
        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass
        
        def exec(self):
            pass
        def exec(self,*args,**kwargs):
            pass
        def run(self):
            self.init()
            print(self.exec())

inf = float("inf")
MOD = (10**9)+7


class UniFind:
    
    def __init__(self, n) -> None:
        self.p = [-1]*n
        self.value = [0]*n

    def merge(self, parent, child, val):
        parent1, pval = self.find(parent)
        child1, cval = self.find(child)
        if parent1 == child1:
            return parent1, False
        pct =  self.p[parent1]+self.p[child1]
        self.p[child1] = parent1
        self.p[parent1]=pct
        self.value[child] = (val+pval-cval)%MOD
        return parent1, True

    def find(self, idx):
        idz = idy = idx
        value = 0
        while self.p[idx] >= 0:
            value = (value+self.value[idx])%MOD
            idx = self.p[idx]
        while idy != idx:
            self.value[idy], value = value, value-self.value[idy]
            self.p[idy], idy = idx, self.p[idy]
        return idy, self.value[idz]



    def algo_view(self):
        root_child=[]
        nodes=[dict(
            title=f'节点{i}{bp("子节点数",-v if v<0 else 1,i)}',
            data=dict(line_title=self.value[i]),
            childs=[]
        ) for i,v in enumerate(self.p)]
        for i,v in enumerate(self.p):
            if v>0 and v!=i:
                nodes[v]['childs'].append(nodes[i])
            else:
                root_child.append(nodes[i])
        return dict(childs=root_child,depth=1)

    def hex_str(self):
        return str(self.p) 


CASE1 ='''
6
0
0
1 2 1
2 1 5 2 2
1 1 2
1 3 4
'''
class Solution(SolutionBase):
    uri = "https://codeforces.com/contest/195/problem/E"
    gameinfo = ('cf',195,'E')
    name = 'CodeForce_195_E 计算树的深度和'
    tags = ['并查集']
    动画演示='http://1.14.93.140:8888/font/dist//index.html?route=algo&py_module=app.yly.algo.bcj.cf_195e'
    has_view = True
    def get_cases(self):
        return [
            dict(input=CASE1,result=30),
        ]
    def init(self, result=0,**kwargs):
        self.n= self.i1()
        self.uf = UniFind(self.n)
        self.lines=self.il(self.n)
        self.result=result
        self.ans=0
        self.pid=0
        self.cid=-1
        self.rid=-1
        self.r_val=-1
        self.weight=-1
    
    def hex_str(self):
        return f'{self.ans}{self.pid}{self.lines}'
    
    def main(self):
        return tree(self.uf)
    
    def left(self):
        a1=lambda: [f"节点{i}:{[vj-(j%2==0) for j,vj in enumerate(l[1:])]}" for i,l in enumerate(self.lines)]+[f'答案: {self.result}']
        a2=lambda: [
            bp("连接父节点",self.pid),
            bp("连接子节点的根节点",[self.rid,self.r_val]),
            bp("连接子节点",self.cid),
            bp("权重",self.weight),
            bp("总和",self.ans),
        ]
        b2=lambda: f"{self.cid}{self.pid}{self.rid}{self.weight}{self.ans}{self.r_val}"
        return [
            divh(
                algo_view=a1,
            ),
            divh(
                algo_view=a2,
                hex_str=b2
            )
        ]
        
    
    def exec(self,**kg):
        self.ans = 0
        while self.pid<len(self.lines):
            ids = self.lines[self.pid]
            for i in range(1,len(ids),2):
                self.cid, self.weight = ids[i]-1, ids[i+1]
                self.rid, self.r_val = self.uf.find(self.cid)
                self.r_val = (self.r_val+self.weight)%MOD
                self.uf.merge(self.pid, self.rid, self.r_val)
                self.ans = (self.r_val+self.ans)%MOD
            self.pid+=1
        return self.ans % MOD
    
    
if __name__ == '__main__':
    Solution().run()

