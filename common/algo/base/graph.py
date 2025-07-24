from collections import defaultdict
import heapq
from typing import List, Dict

from common.algo.base.node import Node


class Graph(Node):
    nodes: Dict[str, "Node"] = Node
    edges = dict()

    def __init__(self, key=None):
        self.key = key

    def load(self):
        self.in_deg = 0
        self.out_deg = 0
        self.childs: Dict[str, Graph] = dict()
        return self

    def reset(self):
        self.edges.clear()
        Graph.nodes = {}
        return self

    def add_node(self, kid):
        if kid not in self.nodes:
            self.nodes[kid] = Graph(kid).load()
        return self.nodes[kid]

    def add_edge(self, f, t, *args):
        fn: Graph = self.add_node(f)
        tn: Graph = self.add_node(t)
        self.edges[f, t] = args
        fn.out_deg += 1
        tn.in_deg += 1
        fn.childs[t] = tn
        return fn, tn

    def load_from_edges(self, edges):
        for i, edge in enumerate(edges):
            self.add_edge(i, *edge)
        return self

    def get_value(self, idx, weight=None, cost=None):
        raise Exception("gg")

    def dijkstra(self, start):
        self.value = dict()
        self.value[start] = self.get_value(start)
        q = [(self.value[start], start)]
        while q:
            cost, u = heapq.heappop(q)
            if cost > self.value[u]:
                continue
            for v, idx, weight, *args in self.g[u]:
                target = self.get_value(v, weight, cost)
                if v not in self.value or target < self.value[v]:
                    self.value[v] = target
                    heapq.heappush(q, (self.value[v], v))
        return self.value

    def tupu(self, indeg_aim=0):
        q: List[Graph] = [v for v in self.nodes.values() if v.in_deg == indeg_aim]
        ans = []
        while q:
            ans.clear()
            q, tmp = [], q
            for x in tmp:
                ans.append(x)
                for y in x.childs.values():
                    y.in_deg -= 1
                    if y.in_deg == indeg_aim:
                        q.append(y)
        return ans

    dis = None

    def bfs(self):
        q: List[Node] = [self]
        self.dis = dict()
        self.dis[self.key] = 0
        while q:
            tmp = q
            q = []
            for c in tmp:
                for n in c.childs.values():
                    if n.key in self.dis:
                        continue
                    self.dis[n.key] = self.dis[c.key] + 1
                    q.append(n)

        return self.dis

    def get_dis(self, y, x):
        if self.nodes[y].dis is None:
            self.nodes[y].bfs()
        return self.nodes[y].dis[x]

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
            for nv in self.g[n]:
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

    def floyd(self, dis, keys):
        for k in keys:
            for i in keys:
                for j in keys:
                    dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])
        return dis

    def eula_time_visit(self, start=0):
        tmstamp = 1
        stk = [start]
        ls = defaultdict(int)
        rs = defaultdict(int)
        c = self
        while stk:
            u = stk.pop()
            if u >= 0:
                ls[u] = tmstamp
                tmstamp += 1
                stk.append(-1 - u)
                for v in c.childs:
                    stk.append(v)
            else:
                rs[-1 - u] = tmstamp
        return ls, rs
