from typing import List,Dict,Optional
from collections import defaultdict, deque,Counter
from itertools import accumulate,product
from functools import lru_cache

import bisect
import sys
import math
import heapq
inf=float("inf")
null=None
true=True
false=False
M=10**9 + 7


class MKAverage:
    @classmethod
    def get_cases(cls):
        return [

         
        ]


    local_debug=None
    def init(self):
        self.local_debug=getattr(self,sys.argv[-1],None)
        if self.local_debug is None:
            print(sys.argv[-1],"not find")

    logs = ""
    def log(self, *s):
        if not self.local_debug or len(self.logs)>=2048:
            return
        self.logs += " ".join([str(v) for v in s])+"\n"
    
    @classmethod
    def run(cls):
        for case in cls.get_cases():
            m,inp,es=case
            r=cls(*inp[0])
            r.init()
            r.logs=""
            r.log(m[0],*inp[0])
            flag=True
            for i in range(1,len(inp)):
                r.log(m[i],inp[i],es[i])
                e=getattr(r,m[i])(*inp[i])       
                
                if not r.diff(e,es[i]):
                    r.check(*case,e)
                    print(r.logs)
                    print(e,es[i])
                    flag=False
                    break
            if not flag:
                break
            
    def diff(self,a,b):
        if isinstance(a,float) and isinstance(b,float):
            return "%.2f"%(a)=="%.2f"%(b)
        return a==b

    



      

if __name__ == '__main__':
    MKAverage.run()



