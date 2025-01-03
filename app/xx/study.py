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

def test_19(func):
    b=time.time()
    for _ in range(10**6):
        func()
    ret=time.time()-b
    print(f'{ret} {func.__name__}')
    return ret

class Study:    
    def loop(self):
        assert test_19(loop1) > test_19(loop)
    def calc(self):
        assert test_19(int_cnt) < test_19(str_cnt)< test_19(str_cnt2)
if __name__=="__main__":
   getattr(Study(),sys.argv[1])()