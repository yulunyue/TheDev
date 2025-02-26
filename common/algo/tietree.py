from typing import List,Dict
from collections import defaultdict

class TieNode:
    idx=0
    cur=None
    son=None
    def __init__(self, key, keys, depth=0, default_value=None, parent=None,root=None) -> None:
        self.key = key
        self.keys = keys
        self.idx=TieNode.idx
        TieNode.idx+=1
        self.childs:Dict[str,TieNode] = {k:None for k in keys}
        self.fail: TieNode = None
        # self.last: TieNode = None
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
        self.fail  = self
        q: List[TieNode] = [] 
        for k in self.childs:
            if self.childs[k] is None:
                self.childs[k] = self
            else:
                self.childs[k].fail  = self
                q.append(self.childs[k])
        while q:
            TieNode.cur = q.pop(0)
            for k, son in TieNode.cur.childs.items():
                if son is None:
                    TieNode.cur.childs[k] = TieNode.cur.fail.childs[k]
                    continue
                TieNode.son = son
                TieNode.son.fail = TieNode.cur.fail.childs[k]
                # son.last = son.fail if son.fail.depth else son.fail.last
                q.append(TieNode.son)

    def k(self,name="tit_node"):
        return f'{self.idx}_{name}'
    
    def __str__(self):
        ret=[
            "" if TieNode.cur is None else str(TieNode.cur.idx),
            "" if TieNode.son is None else str(TieNode.son.idx)
        ]
        vt=set()
        def dfs(n:TieNode):
            if n is None or n.idx in vt:
                return
            ret.append(f'{n.idx}')
            vt.add(n.idx)
            for cc in n.childs.values():
                dfs(cc)
        dfs(self)
        return "".join(ret)
    

    def get_title_keys(self):
        return ['key','depth']
    
    def get_nodes(self):
        from common.algo.manage import bp
        color = '#fff'
        if TieNode.cur==self:
            color='#999'
        elif TieNode.son==self:
            color='#ccc'
        return dict(data=[
            bp(k,getattr(self,k),self.k(k))
            for k in self.get_title_keys()
        ],color=color)
    
    def graph_view(self):
        nodes,edges=dict(),[]
        self.get_graph(nodes,edges)
        return dict(data=dict(
            edges=edges,
            nodes=nodes,
        ))
    
    def get_graph(self,nodes,edges:list):
        kp=self.k()
        if kp in nodes:
            return
        nodes[kp]=self.get_nodes()
        # if self.fail:
        #     edges.append([kp,self.fail.k(self.fail.idx),self.fail.key])
        for v in self.childs.values():
            if v is None:
                continue
            if v.key:
                edges.append([kp,v.k()])
            v.get_graph(nodes,edges)
 