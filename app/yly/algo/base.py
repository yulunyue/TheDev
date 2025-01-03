import sys
inf = float("inf")
MOD = (10**9)+7

def fmax(a,b,*args):return a if a>b else b
def fmin(a,b,*args):return a if a<b else b
class View:
    def __init__(self,*args,**kw) -> None:
        pass
class SolutionBase:
    DEV = False
    inputs=[]
    results=[]
    uri=""
    def input(self):
        self.inputs.append(input())
        return self.inputs[-1]
    def error(self,*args):
        print("\n".join(self.inputs), file=sys.stderr, flush=True)
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
        self.exec()
    def run_cls(self):
        pass
    def output(self,*args):
        print(*args)
        sys.stdout.flush()





