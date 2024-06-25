
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
        self.size=size*4
        self.store=defaultdict(lambda :default_value)
    def update_min_dp(self,o,l,r,v,L,R):
        if l==L and r==R:
            self.store[o]=min(self.store[o],v)
            return self.store[o]
        mid=(L+R)//2
        if r<=mid:
            ret=self.update_min_dp(o*2,l,r,L,mid)
        elif mid<l:
            ret=self.update_min_dp(o*2+1,l,r,mid+1,R)
        else:
            self.update_min_dp(o*2,l,mid,L,mid)
            self.update_min_dp(o*2+1,mid+1,r,mid+1,R)
        return self.store[o]
    
    def update_min(self,l,r,v):
        self.update_min_dp(1,l,r,v,0,self.size)

    def update_sum_dq(self,o,l,r,L,R,v):
        if l<=L and R<=l:
            self.store[o]+=v
            return 
        mid=(L+R)//2
        if r<=mid:
            self.update_sum_dq(o*2,l,r,L,mid,v)
        elif mid<l:
            self.update_sum_dq(o*2+1,l,r,mid+1,R,v)
        else:
            self.update_min_dp(o*2,l,mid,L,mid,v)
            self.update_min_dp(o*2+1,mid+1,r,mid+1,R,v)
        self.store[o]=self.store[o*2]+self.store[o*2+1]
    
    def update_sum(self,l,value):
        self.update_sum_dq(1,l,l,0,self.size,value)
   
    def query_sum_dq(self,o,l,r,L,R):
        if l==L and r==R:
            return self.store[o]
        mid=(L+R)//2
        if r<=mid:
            return self.query_sum_dq(o*2,l,r,L,mid)
        elif mid<l:
            return self.query_sum_dq(o*2+1,l,r,mid+1,R)
        return self.query_sum_dq(o*2,l,mid,L,mid)+self.query_sum_dq(o*2+1,mid+1,r,mid+1,R)
            

    def query_sum(self,l,r):
        if r<l:
            return 0
        return self.query_sum_dq(1,l,r,0,self.size)