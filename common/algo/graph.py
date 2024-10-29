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


class AlphaBate:
    '''
                               0,3

          1,2                  2,6               3,3

    4,8   5,2   6,7       7,1  8,?  9,?     10,3  11,6   12,9   


    '''

    def __init__(self, max_depth, max_time=inf) -> None:
        self.max_depth = max_depth
        self.max_time = max_time

    next_values = [8, 2, 7, 1, 3, 6, 9]

    def evaluate(self):
        return self.next_values.pop(0)

    def end_search(self, depth):
        return depth >= self.max_depth

    def do(self, *args):
        pass

    def undo(self, *args):
        pass

    def get_moves(self):
        return [None]*3

    def search(self, depth=0, alpha=-inf, bate=inf) -> None:
        if self.end_search(depth):
            return self.evaluate()
        best_mv = None
        for mv in self.get_moves():
            self.do(*mv)
            _, val = self.search(depth=depth+1, alpha=-bate, bate=-alpha)
            val = -val
            self.undo(*mv)
            if val >= bate:
                alpha = bate
                best_mv = mv
                break
            if val > alpha:
                alpha = val
                best_mv = mv
        return best_mv, alpha

    def serach_limit_time(self):
        best_mv, best_score = None, -inf
        for i in range(self.max_depth):
            pass
