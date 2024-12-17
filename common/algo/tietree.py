from typing import List,Dict
from collections import defaultdict

class TieNode:
    idx=0
    def __init__(self, key, keys, depth=0, default_value=None, parent=None,root=None) -> None:
        self.key = key
        self.keys = keys
        self.idx=TieNode.idx
        TieNode.idx+=1
        self.childs:Dict[str,TieNode] = {k:None for k in keys}
        self.fail: TieNode = None
        self.last: TieNode = None
        self.root: TieNode = None
        self.parent: TieNode = parent
        self.depth = depth
        self.default_value = default_value
        self.value = default_value

    def add(self, s):
        tmp = self
        for i in s:
            if tmp.childs[i] is None:
                tmp.childs[i] = TieNode(
                    i,self.keys,
                    depth=tmp.depth+1,
                    default_value=self.default_value,
                    parent=self,
                    root=self
                )
            tmp = tmp.childs[i]
        return tmp

  

    def build_fail(self):
        self.fail = self.last = self
        q: List[TieNode] = [] 
        for k in self.childs:
            if self.childs[k] is None:
                self.childs[k] = self
            else:
                self.childs[k].fail = self.childs[k].last = self
                q.append(self.childs[k])
        while q:
            cur = q.pop(0)
            for k, son in cur.childs.items():
                if son is None:
                    cur.childs[k] = cur.fail.childs[k]
                    continue
                son.fail = cur.fail.childs[k]
                son.last = son.fail if son.fail.depth else son.fail.last
                q.append(son)

    def k(self,name):
        return f'{self.idx}_{name}'
    
    
    def __str__(self) -> str:
        ret=[self.key]
        ret.extend(str(c) for c in self.childs)
        return "".join(ret)
    
    def get_title_keys(self):
        return ['key']
    
    def tree_view(self):
        ret=dict(
            data=[
                self.k(k) for k in self.get_title_keys()
            ],
            childs=[c.tree_view() for c in self.childs.values()],
            key=self.k(f'{self.key}_node')
        )
        return ret
    
    def get_nodes(self):
        from app.yly.algo.manage import bp
        return dict(data=[
            bp('',self.idx,self.k('idx')),
        ])
    def graph_view(self):
        nodes,edges=dict(),[]
        self.get_graph(nodes,edges)
        return dict(data=dict(
            edges=edges,
            nodes=nodes,
        ))
    
    def get_graph(self,nodes,edges:list):
        kp=self.k(self.idx)
        if kp in nodes:
            return
        nodes[kp]=self.get_nodes()
        for v in self.childs.values():
            if v is None:
                continue
            edges.append([kp,v.k(v.idx),v.key])
            v.get_graph(nodes,edges)
 