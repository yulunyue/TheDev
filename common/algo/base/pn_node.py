class PnNode:
    left:"PnNode"=None
    right:"PnNode"=None
    def __init__(self,v):
        self.value=v
    @class_method
    def make(array):
        ret=[]
        for i,v in enumerate(array):
            n=PnNode(v)
            if i!=0:
                n.set_left(ret[-1])
            ret.append(n)
        return ret
    def set_left(self,r):
        self.left=r
        if r:
            r.right=self
    def remove(self):
        self.left

