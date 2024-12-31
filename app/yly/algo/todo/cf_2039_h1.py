from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
from common.algo.math_util import Comb
MOD=(10**9)+7
inf = float("inf")
from collections import defaultdict
class Solution(SolutionBase):
    uri='https://codeforces.com/problemset/problem/2039/H1'
    def get_cases(self):
        return [
            dict(array=[2, 1, 0, 3],result=0),
            dict(array=[2, 1, 0],result=0),
            dict(array=[3, 1, 0, 2],result=0),
            dict(array=[2, 3, 4, 1, 0], result=0),
            dict(array=[2, 4, 3, 1, 0], result=0),
            dict(array=[2, 1, 0, 3, 4, 5], result=0),
            dict(array=[2, 1, 0, 3, 4, 5], result=0),

     
        ]


    def performSwaps(self,skips:List[int]):
        o = []
        skips = skips[::-1]
        i = 0
        while i+1<self.n:
            if skips:
                if i+1 == skips[-1]:
                    i+=2
                    skips.pop()
                    o.append("DDRR")
                    continue
            i+=1
            o.append("DR")
        return o
    
    def init(self, array, **kwargs):
        self.array=array

    def execute(self):
        out=[]
        a = self.array
        n=self.n=len(a)
        min_a=min(a)
        start=a.index(min_a)
        
        while True:
            exit_flag=True         
            self.log(start,a)
            for i in range(n-1):
                if a[(start+i)%n]>a[(start+i+1)%n]:
                    exit_flag=False
                    break
            if exit_flag:
                break
            b=[]
            swaps = []
            for i in range(1,n-1,2):
                if a[i]<=a[i+1] or i+1 == start%n:
                    b.append(a[i])
                    b.append(a[i+1])
             
                else:
                    swaps.append(i)
                    b.append(a[i+1])
                    b.append(a[i])
            if n%2==0:
                b.append(a[-1])
            b.append(a[0])
            out.append("".join(self.performSwaps(swaps)))
            self.log(out[-1],swaps)
            start =(start-1+n)%n
            a = b
            # self.log(out[-1])
            
        for _ in range(start):
            out.append("DR"*(n-1))
        self.output(len(out))
        for mv in out:
            self.output(mv)
        return len(out)
    
    def baoli(self):
        for n in list(range(8,9)):
            max_t=defaultdict(list)
            cms=Comb().make_array(list(range(0,n)))
            for a in cms:
                self.array=a
                max_t[self.execute()].append(a)
            idx=max(max_t.keys())
            self.log(f'---{n}---')
            for v in max_t[idx]:
                self.log(v)
            self.log(idx)

    
    def exec(self):
        for _ in range(self.i1()):
            self.i1()
            self.init(self.il())
            self.execute()

        



if __name__=='__main__':
    Solution().run()