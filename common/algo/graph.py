from collections import defaultdict
import heapq
from typing import List
inf = float("inf")


def dijkstra(g, start):
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    q = [(0, start)]
    while q:
        cost, u = heapq.heappop(q)
        if cost > dist[u]:
            continue
        for v, weight in g[u]:
            target = cost + weight
            if target < dist[v]:
                dist[v] = target
                heapq.heappush(q, (dist[v], v))

    return dist


def tarjan(g, b, init_ct=0):
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


def floyd(dis, keys):
    for k in keys:
        for i in keys:
            for j in keys:
                dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])
    return dis


class Graph:
    def __init__(self):
        self.g=[]

    def load_from_edges(self,edges):
        self.g = [[] for _ in range(len(edges))]
        for x, y in edges:
            self.g[x].append(y)
            self.g[y].append(x)  # 建树
        return self
    
    def algo_view(self):
        ret = dict(
            
        )
        def dfs(c,p,v):
            v['title']=c
            v['childs']=[]
            for n in self.g[c]:
                if p==n:continue
                tmp=dict()
                v['childs'].append(tmp)
                dfs(n,c,tmp)
        dfs(0,-1, ret)
        return ret
    
    def hex_str(self):
        return str(self.g)
        
