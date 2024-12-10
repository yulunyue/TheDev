from collections import defaultdict
import heapq
from typing import List
inf = float("inf")






class Graph:
    def __init__(self,value=0):
        self.g = defaultdict(list)
        self.edges = []
        self.value = defaultdict(lambda: value)
    
    def set_values(self,values):
        for i,v in enumerate(values):
            self.value[i]=v
        return self


    def add_edge(self,idx,y,x,valuey=None,valuex=None):
        self.g[x].append([y,idx,valuey])
        self.g[y].append([x,idx,valuex])  # 建树
        self.edges.append([y,x,idx,valuey,valuex])
    
    def load_from_edges(self,edges):
        for i,edge in enumerate(edges):
            self.add_edge(i,*edge)
        return self
    def key(self,k):
        return f'graph_{k}'
    
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
        return f'{self.edges}{self.value}'
    
    def dijkstra(self, start):
        
        self.dist[start] = 0
        q = [(0, start)]
        while q:
            cost, u = heapq.heappop(q)
            if cost > self.dist[u]:
                continue
            for v, weight in self.g[u]:
                target = cost + weight
                if target < self.dist[v]:
                    self.dist[v] = target
                    heapq.heappush(q, (self.dist[v], v))
        return self.dist


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