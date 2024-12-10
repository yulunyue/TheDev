class Fenwick:
    '''
                    16
        8
    4        12            20
  2   6   10    14     18
 1 3 5 7 9 11 13  15 17  19  21
    '''

    def __init__(self) -> None:
        self.i = 0 
        self.size = 1
        self.array = []

    def set_size(self, size,default_value=0):
        self.array = [default_value]*(size+1)
        self.size = size+1
        
    def update_value(self, i, v):
        self.i = i
        while self.i < self.size:
            self.array[self.i] = v(self.array[self.i])
            self.i += self.i & -self.i

    def query_value(self, i, f, init_value):
        ret = init_value
        self.i=i
        while self.i > 0:
            ret = f(ret, self.array[self.i])
            self.i &= self.i - 1
        return ret

    def query_sum(self, l,r=None,init_value=0):
        ret=self.query_value(l+1, lambda a, b: a+b, init_value)
        if r is not None:
            return self.query_value(r+1, lambda a, b: a+b, init_value)-ret
        return ret
    
    def add_value(self, l, v):
        self.update_value(l+1, lambda a: a+v)

    def graph_view(self):
        from app.yly.algo.manage import bp
        nodes={
            f'fen_{i}':dict(data=[
                bp('',i,f"fenwick__{i}"),
                bp('value',self.array[i],f"fenwick_value_{i}")
            ]) 
            for i in range(1,self.size)
        }
        edges=[]
        for i in range(1,self.size):
            k = i+ (i & -i)
            if k<self.size:
                edges.append([f'fen_{k}',f'fen_{i}','up'])
            k = i &(i - 1)
            if k>0:
                edges.append([f'fen_{i}',f'fen_{k}','query'])
        return dict(data=dict(nodes=nodes,edges=edges))
    
    def __str__(self) -> str:
        return str(self.array)