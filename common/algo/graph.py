from collections import defaultdict


class Graph:
    def __init__(self) -> None:
        pass

    def load_from_g(self,g):
        self.g=g
        self.keys=list(range(len(g)))
        return self
    
    def load_from_edge(self, edges):
        self.g=defaultdict(lambda :defaultdict(int))
        self.keys=[]
        for f,t in edges:
            self.keys.append(f)
            self.keys.append(t)
            self.g[f][t]=1
            self.g[t][f]=1
        self.keys=list(set(self.keys))        
        return self
    
    def log(self,*args):
        pass
    
    def tarjan(self,b,init_ct=0):
        low=defaultdict(lambda: init_ct)
        vt=defaultdict(lambda: init_ct)
        self.ct=init_ct
        points=dict()
        edges=[]
        def dfs(n,p):
            # self.log(p,n)
            self.ct+=1
            vt[n]=low[n]=self.ct
            c=0
            for nv in self.g[n]:
                if p==nv:
                    continue
                if vt[nv]==init_ct:
                    c+=1
                    dfs(nv,n)
                    low[n]=min(low[nv],low[n])
                    self.log('b1',n,nv,low[nv],low[n])
                    if vt[n]<=low[nv] and p !=-1:
                        points[n]=True
                    if vt[n]<low[nv]:
                        edges.append([n,nv])
                else:
                    low[n]=min(low[n],vt[nv])
                    self.log('b2',n,nv,vt[nv],low[n])
            if c>=2 and p == -1:
                points[n]=True
        dfs(b,-1)
        return edges,points,low
