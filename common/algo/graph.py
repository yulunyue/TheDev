from collections import defaultdict
import heapq
from typing import List, Dict
inf = float("inf")

class GraphNode:
    nodes=dict()
    edges=dict()
    def __init__(self,key=None):
        self.key=key
        self.childs:Dict[str,GraphNode]=dict()
    
    def init(self):
        self.edges.clear()
        self.nodes.clear()
        return self
    
    def add_node(self,kid):
        if kid not in self.nodes:
            self.nodes[kid]=GraphNode(kid)
        return self.nodes[kid]
    
    def add_edge(self,f,t,*args):
        fn:GraphNode=self.add_node(f)
<<<<<<< HEAD
        tn=self.add_node(t)
        fn.childs[t]=tn
        self.edges[f,t]=args
        return self

=======
        tn:GraphNode=self.add_node(t)
        self.edges[f,t]=args
        fn.childs[t]=tn
        return fn,tn
    
>>>>>>> 28cce18b740a00a67ff9acb42e95ade04d62f6fb
    def set_values(self,values):
        for i,v in enumerate(values):
            self.value[i]=v
        return self

    
    def load_from_edges(self,edges):
        for i,edge in enumerate(edges):
            self.add_edge(i,*edge)
        return self
    
    def get_title_key(self):
        return ['value']

    def get_nodes(self,i):
        from app.yly.algo.manage import bp
        return dict(data=[
            bp('',i,self.key(i)),
        ]+[
            bp(k,getattr(self,k)[i],self.key(f'{k}_{i}')) 
            for k in self.get_title_key()
        ])
    
    def get_edges(self):
        return [[self.key(e[0]),self.key(e[1])]+e[2:] for e in self.edges]

    def graph_view(self):
        return dict(data=dict(
            edges=self.get_edges(),
            nodes={self.key(k):self.get_nodes(k) for k in self.g},
        ))
    
    def __str__(self):
        return f'{self.edges}'
    
    def get_value(self,idx, weight=None,cost=None):
        raise Exception("gg")
    
    def dijkstra(self, start):
        self.value=dict()
        self.value[start] = self.get_value(start)
        q = [(self.value[start], start)]
        while q: 
            cost, u = heapq.heappop(q)
            if cost > self.value[u]:
                continue
            for v, idx, weight,*args in self.g[u]:
                target = self.get_value(v,weight,cost)
                if v not in self.value or target < self.value[v]:
                    self.value[v] = target
                    heapq.heappush(q, (self.value[v], v))
        return self.value

    def bfs(self,start):
        q=[start]
        dis=dict()
        l=0
        dis[start]=l
        while q:
            tmp=q
            q=[]
            for c in tmp:
                for n,*args in self.g[c]:
                    if n in dis:
                        continue
                    dis[n]=l+1
                    q.append(n)
            l+=1
        return dis
    
    def get_dis(self,y,x):
        if y in self.dis:
            return self.dis[y].get(x,inf)
        if x in self.dis:
            return self.dis[x].get(y,inf)
        self.dis[y]=self.bfs(y)
        return self.dis[y].get(x)
    
    def tarjan(self, b, init_ct=0):
        low = defaultdict(lambda: init_ct)
        vt = defaultdict(lambda: init_ct)
        ct = init_ct
        points = dict()
        edges = []

        def dfs(n, p):
            nonlocal ct
            ct += 1
            vt[n] = low[n] = ct
            c = 0
            for nv in g[n]:
                if p == nv:
                    continue
                if vt[nv] == init_ct:
                    c += 1
                    dfs(nv, n)
                    low[n] = min(low[nv], low[n])
                    if vt[n] <= low[nv] and p != -1:
                        points[n] = True
                    if vt[n] < low[nv]:
                        edges.append([n, nv])
                else:
                    low[n] = min(low[n], vt[nv])
            if c >= 2 and p == -1:
                points[n] = True
        dfs(b, -1)
        return edges, points, low


    def floyd(self,dis, keys):
        for k in keys:
            for i in keys:
                for j in keys:
                    dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])
        return dis
    

    def eula_time_visit(self,start=0):
        tmstamp = 1
        stk = [start]
        ls=defaultdict(int)
        rs=defaultdict(int)
        c =self
        while stk:
            u = stk.pop()
            if u >= 0:
                ls[u] = tmstamp
                tmstamp += 1
                stk.append(-1-u)
                for v in c.childs:
                    stk.append(v)
            else:
                rs[-1-u] = tmstamp
        return ls,rs