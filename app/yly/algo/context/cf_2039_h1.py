from app.yly.algo.manage import SolutionBase,View
from typing import Dict,List
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
CASE1=dict(
    input='''3
2
1 2
3
2 1 3
4
3 2 3 4
''',
result='''0
2
DRDR
RRDD
3
RRDRDD
DRDDRR
DDRRRD''')
class Solution(SolutionBase):
    uri='https://codeforces.com/problemset/problem/2039/H1'
    def get_cases(self):
        return [
            CASE1
        ]
    def init(self, *args, **kwargs):
        self.inputs=[]

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
    
    def calc(self,a:List[int]):
        out=[]
        n=self.n=len(a)
        min_a=min(a)
        start=a.index(min_a)
        while True:
            exit_flag=True
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
                    continue
                swaps.append(i)
                b.append(a[i+1])
                b.append(a[i])
            if n%2==0:
                b.append(a[-1])
            b.append(a[0])
            out.append("".join(self.performSwaps(swaps)))
            start -= 1
            start %= n
            a = b[:]
            
        for _ in range(start):
            out.append("DR"*(n-1))
        self.output(len(out))
        for mv in out:
            self.output(mv)

    def exec(self):
        for _ in range(self.i1()):
            self.i1()
            self.calc(self.il())
        return "\n".join(self.results)
        



if __name__=='__main__':
    Solution().run()