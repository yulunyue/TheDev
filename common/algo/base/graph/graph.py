from collections import defaultdict
import heapq
from typing import List, Dict


class Graph:

    def __init__(self, *args):
        self.load(*args)

    def load(self, *args):
        self.in_deg = defaultdict(int)
        self.out_deg = defaultdict(int)
        return self

    def get_value(self, f, t, cost=0):
        raise Exception("gg")

    def get_nexts(self, u):
        return self.g[u]

    def set_edges(self, g):
        self.g = g
        return self

    def dijkstra(self, start, target=None):
        value = dict()
        value[start] = self.get_value(start, start)
        q = [(value[start], start)]
        while q:
            cost, u = heapq.heappop(q)
            if cost > value[u]:
                continue
            if u == target:
                break
            for v in self.get_nexts(u):
                cost2 = self.get_value(u, v, cost=cost)
                if v not in value or cost2 < value[v]:
                    value[v] = cost2
                    heapq.heappush(q, (value[v], v))
        return value

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
