from collections import defaultdict
import heapq
from typing import List
inf = float("inf")






class Graph:
    def __init__(self,value=inf):
        self.g = defaultdict(list)
        self.edges = []
        self.values = defaultdict(lambda: value)
    
    def set_values(self,values):
        for i,v in enumerate(values):
            self.values[i]=v
        return self
    def add_edge(self,idx,y,x,valuey=None,valuex=None):
        self.g[x].append([y,idx,valuey])
        self.g[y].append([x,idx,valuex])  # 建树
        self.edges.append([y,x,idx,valuey,valuex])
    
    def load_from_edges(self,edges):
        for i,edge in enumerate(edges):
            self.add_edge(i,*edge)
        return self
    
    def to_view(self):
        return dict(data=dict(
            edges=self.edges,
            nodes=self.values,
        ))
    
    def __str__(self):
        return str(self.edges)
    
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