from collections import defaultdict
import heapq


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
