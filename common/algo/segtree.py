
from collections import defaultdict

class IntervalTree:
    '''
                    16
        8
    4        12            20
  2   6   10    14     18
 1 3 5 7 9 11 13  15 17  19  21
    '''
    def __init__(self,size,default_value) -> None:
        self.array=[default_value]*size
        self.size=size

    def update_min(self,l,v):
        while l<self.size:
            self.array[l]=v
            l+=l&-l


    def query_min(self,l):
        ret=self.array[l]
        while l>0:
            ret=min(self.array[l],ret)
            l-=l&-l
        return ret

class SegTree:
    def __init__(self,size,default_value) -> None:
        self.size=size
        self.store=defaultdict(lambda :default_value)
    def update_min_dp(self,o,l,r,v,L,R):
        if l==L and r==R:
            self.store[o]=min(self.store[o],v)
            return self.store[o]
        mid=(L+R)//2
        if r<=mid:
            ret=self.update_min_dp(o*2,l,r,L,mid)
        elif mid<=l:
            ret=self.update_min_dp(o*2+1,l,r,mid,R)
        else:
            self.update_min_dp(o*2,l,mid,L,mid)
            self.update_min_dp(o*2+1,mid+1,r,mid+1,R)
        return self.store[o]
    def update_min(self,l,r,v):
        self.update_min_dp(1,l,r,v,0,self.size)