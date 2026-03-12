class Solution:
    def get_cases(self):
        return dict(case0=n = 3, edges = [[0,1,2,1],[1,2,3,0]], k = 1)
    def maxStability(self, n: int, edges: List[List[int]], k: int) -> int:
        ufm=Uf()
        mn=CT.inf
        h=[]
        for f,t,w,m in edges:
            if m:
                if ufm.merge(f,t):
                    return -1
                mn=CT.min(mn,w)
            else:
                heapq.heapqpush(h,[w,f,t])
        if ufm.size==n:
            return mn
        d=[]
        while h and ufm.size<n:
            w,f,t=heapq.heapqpop(h)
            if ufm.merge(f,t):
                d.append(w)
        mn=CT.max(mn,d[0]*2)
        if k<d:
            return CT.min(mn,d[k-1])
        return mn

