from typing import List,Dict
class UniFind:
    def __init__(self) -> None:
        self.p = dict()
        self.size = dict()

    def merge(self, parent, child):
        parent1 = self.find(parent)
        child1 = self.find(child)
        if parent1 == child1:
            return parent1, False
        self.p[child1] = parent1
        self.size[parent1] += self.size[child1]
        self.size[child1] = 0
        return parent1, True

    def find(self, v):
        if v not in self.p:
            self.p[v] = v
            self.size[v] = 1
        if self.p[v] != v:
            self.p[v] = self.find(self.p[v])
        return self.p[v]

    def update(self):
        for k in self.p:
            self.find(k)

    def get_pkeys(self):
        return set(list(self.p.values()))
    
    def algo_view(self):
        root_child=[]
        nodes=[dict(title=f'{i}',childs=[]) for i,v in enumerate(self.p)]
        for i,v in enumerate(self.p):
            if v==i:
                root_child.append(nodes[i])
            else:
                nodes[v]['childs'].append(nodes[i])
        return dict(childs=root_child,title='root')

    def hex_str(self):
        return str(self.p) 

        