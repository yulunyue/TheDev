
class Solution:
    def minimumFlips(self, n: int, edges: List[List[int]], start: str, target: str) -> List[int]:
        g=[[] for _ in range(n)]
        v=[0 if start[i]==target[i] else 1 for i in range(n)]
        for f,t in edges:
            g[f].append(t)
            g[t].append(f)


