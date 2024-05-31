from collections import defaultdict

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Graph:
    def __init__(self,g) -> None:
        self.g=g

    def tarjan(self,b):
        low=defaultdict(int)
        vt=defaultdict(int)
        self.ct=1
        points=dict()
        edges=[]
        def dfs(n,p):
            vt[n]=low[n]=self.ct
            self.ct+=1
            c=0
            for nv in self.g[n]:
                if p==nv:
                    continue
                if vt[nv]==0:
                    c+=1
                    dfs(nv,n)
                    low[n]=min(low[nv],low[n])
                    if vt[n]<=low[nv] and p !=-1:
                        points[n]=True
                    if vt[n]<low[nv]:
                        edges.append([n,nv])
                else:
                    low[n]=min(low[n],vt[nv])
            if c>=2 and p == -1:
                points[n]=True
        dfs(b,-1)
        return edges,points
