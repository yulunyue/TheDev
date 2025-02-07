import sys
import json
import bisect
from functools import lru_cache
from typing import Dict,List
from collections import defaultdict
inf = float("inf")
MOD = (10**9)+7

def fmax(a,b,*args):return a if a>b else b
def fmin(a,b,*args):return a if a<b else b
class SolutionBase:
    DEV = False
    inputs=[]
    results=[]
    uri=""
    def input(self):
        self.inputs.append(input())
        return self.inputs[-1]
    def error(self,**kw):
        kw.update(inputs=self.inputs)
        print(json.dumps(kw), file=sys.stderr, flush=True)
        self.inputs.clear()
        
    def i1(self):
        return int(self.input())
    
    def il(self):
        return [int(v) for v in self.input().split(' ')]
    
    def log(self, *args, **kwargs):
        pass

    def init(self,*args,**kwargs):
        pass
    
    def execute(self, *args, **kwargs):
        pass

    def exec(self):
        pass

    def run(self):
        ret=self.exec()
        if ret is not None:
            self.output(ret)
            
    def run_cls(self):
        pass
    def output(self,*args):
        print(*args)
        sys.stdout.flush()





