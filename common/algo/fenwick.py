class Fenwick:
    '''
                    16
        8
    4        12            20
  2   6   10    14     18
 1 3 5 7 9 11 13  15 17  19  21
    '''

    def __init__(self, size,default_value=0) -> None:
        self.size = size + 1
        self.array = [default_value]*self.size
        self.i = 0 
        
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

    def to_view(self):
        from app.yly.algo.manage import bp
        nodes=[
            dict(title=[
                bp('',i,f"fenwick_{i}"),
                bp('value',self.array[i],f"fenwick_value_{i}")
            ],childs=[]) 
            for i in range(self.size)
        ]
        flag=[True]*self.size
        flag[0]=False
        for j in range(1,self.size):
            i=j
            while i < self.size:
                k = i+ (i & -i)
                
                if k>=self.size:
                    break
                flag[i]=False
                nodes[k]['childs'].append(nodes[i])
                i = k
            i=j
            while i > 0:
                k = i &(i - 1)
                if k<=0:
                    break
                nodes[i]['childs'].append(nodes[k])
                flag[k]=False
                i = k
        return dict(childs=[nodes[i] for i in range(self.size) if flag[i]],depth=1)
    
    def __str__(self) -> str:
        return str(self.array)