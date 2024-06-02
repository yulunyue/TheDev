class UniFind:
    def __init__(self,r) -> None:
        self.p=dict()
        self.size=dict()
        for v in r:
            self.p[r]=v
            self.size[v]=1

    def merge(self,f,t):
        f1=self.find(f)
        t1=self.find(t)
        if f1==t1:
            return False
        self.p[f1]=t1
        self.size[t1]+=self.size[f1]
        self.size[f1]=0
        return True
    
    def find(self,v):
        if self.p[v]!=v:
            self.p[v]=self.find(self.p[v])
        return self.p[v]
    
    def update(self):
        for k in self.p:
            self.find(k)

    def get_pkeys(self):
        return set(list(self.p.values()))