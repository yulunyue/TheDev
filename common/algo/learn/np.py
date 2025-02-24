import random

class Array:
    def set_shape(self,shape):
        self.shape=shape
        self.size=1
        for v in self.shape:
            self.size*=v
        self.data=[0]*self.size
        return self

    def fill(self,v):
        self.data=[v]*self.size
        return self
    
    def __getitem__(self,v):
        print(v,self.shape,self.size)
        return self.data[v]

def zeros(shape):
    return Array().set_shape(shape).fill(0)

def argmax(a:Array):
    pass