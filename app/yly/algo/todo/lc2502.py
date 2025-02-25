from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null
class Allocator(SolutionBase):
    def get_cases(self):
        return [
            dict(
                methods=
["Allocator", "allocate", "allocate", "allocate", "freeMemory", "allocate", "allocate", "allocate", "freeMemory", "allocate", "freeMemory"],params=
[[10], [1, 1], [1, 2], [1, 3], [2], [3, 4], [1, 1], [1, 1], [1], [10, 2], [7]],
result=[None, 0, 1, 2, 1, 3, 1, 6, 3, -1, 0]
            )
        ]
    
    def  __init__(self,n):
        self.array=[[0,n]]
        self.free=defaultdict(list)

    
    def allocate(self, size: int, mID: int) -> int:
        for i,(l,c) in enumerate(self.array): 
            if c >= size:
                self.array.pop(i)
                if c>size:
                    self.array.insert(i,[l+size,c-size])
                self.free[mID].append([l,size])
                return l
            # self.log(f'{self.array}\n{self.free}')
            
        return -1
    
    def freeMemory(self, mID: int) -> int:
        ans=0
        # self.log(f'{self.array} {self.free[mID]}')
        while self.free[mID]:
            c,a=self.free[mID].pop(),self.array
            ans+=c[1]
            i=bisect.bisect_left(a,c)
            if i>0 and sum(a[i-1])>=c[0]:
                a[i-1][1]+=c[1]
                i=i-1
            else:
                a.insert(i,c)
            if i+1<len(a) and sum(a[i])>=a[i+1][0]:
                a[i][1]+=a.pop(i+1)[1]            
        # self.log(f'{self.array}')
        return ans



if __name__=='__main__':
    Allocator.run_cls()