import time
import sys
def loop1():
    ret=[]
    for i in range(40):
        if i%2==0:
            ret.append(i)
    return ret

def loop():
    return [i for i in range(40) if i%2==0]

def int_cnt():
    a,b,c=12,23,34
    return a*9+b*3+c

def str_cnt():
    a,b,c="12","23","34"
    return f'{a},{b},{c}'

def str_cnt2():
    a,b,c="12","23","34"
    return ','.join([a,b,c])

def test(func,num=7):
    b=time.time()
    for _ in range(10**num):
        func()
    ret=time.time()-b
    print(f'{ret} {func.__name__}')
    return ret

def test5(func):
    return test(func,num=5)
def test6(func):
    return test(func,num=6)
class A:
    def __init__(self) -> None:
        self.v=1

    @property
    def a(self):
        return sum(list(range(100)))
    
    def b(self):
        return sum(list(range(100)))

class Study:    
    def loop(self):
        assert test(loop1) > test(loop)
    def calc(self):
        assert test(int_cnt) < test(str_cnt)< test(str_cnt2)
    def class_test(self):
        a=A()
        assert test6(lambda :a.a+1)>test6(lambda :a.b()+1)
    def cmp(self):
        def max_1(a,b):
            return a if a>b else b
        def max_0(a,b):
            c=a
            if a>b:
                c=b
            return c
        def max_2(a,b):
            return max(a,b)
    
        assert test6(lambda :max_2(1,0))>=test6(lambda :max_0(1,0))
        assert test6(lambda :max_0(1,0))<=test6(lambda :max_1(1,0))
        assert test6(lambda :max_0(0,1))>=test6(lambda :max_1(0,1))
        
if __name__=="__main__":
   getattr(Study(),sys.argv[1])()