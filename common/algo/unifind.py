from typing import List,Dict
class UniFind:
    def __init__(self,n=None) -> None:
        self.p = dict()
        self.size = dict()
        if isinstance(n,int):
            self.load(n)
    def load(self,n):
        for v in range(n):
            self.find(v)


    def merge(self, parent, child):
        parent1 = self.find(parent)
        child1 = self.find(child)
        if parent1 == child1:
            return parent1, False
        self.p[child1] = parent1
        self.size[parent1] += self.size[child1]+1
        self.size[child1] = 0
        return parent1, True

    def find(self, v):
        if v not in self.p:
            self.p[v] = v
            self.size[v] = 0
        if self.p[v] != v:
            self.p[v] = self.find(self.p[v])
        return self.p[v]

    def update(self):
        for k in self.p:
            self.find(k)

    def get_pkeys(self):
        return set(list(self.p.values()))
    
    def get_node(self,i):
        from app.yly.algo.manage import bp
        return dict(
            title=[
                bp('',i,f"bcj_{i}"),
                bp("size",self.size.get(i,0),f'gcj_size_{i}'),
            ],
            childs=[]
        ) 

    def to_view(self):
        nodes = {k:self.get_node(k) for k in self.p}
        childs = []
        for k,v in self.p.items():
            if k==v:
                childs.append(nodes[k])
                continue
            nodes[k]['childs'].append(nodes[v])
        return dict(childs=childs, depth=1)

    def __str__(self):
        return f'{self.p}'

        