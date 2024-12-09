
inf = float("inf")
MOD = (10**9)+7

def fmax(a,b,*args):return a if a>b else b
def fmin(a,b,*args):return a if a<b else b
class View:
    def __init__(self,*args,**kw) -> None:
        pass
class SolutionBase:
    DEV = False
    
    def input(self):
        return input()

    def i1(self):
        return int(self.input())
    
    def il(self,n):
        return [[int(v) for v in self.input().split(' ')] for _ in range(n)]
    
    def log(self, *args, **kwargs):
        pass

    def init(self,*args,**kwargs):
        pass
    
    def execute(self, *args, **kwargs):
        pass

    def exec(self):
        pass

    def run(self):
        print(self.exec())

  



