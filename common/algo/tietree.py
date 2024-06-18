class TieTree:
    END='_END'
    def __init__(self,size) -> None:
        self.size=size
        self.map=dict()
    def get_num_str(self,s:int):
        ss=bin(s)[2:]
        s1='0'*(self.size-len(ss))+ss
        return s1
    def add(self,s:int):
        tmp=self.map
        s1=self.get_num_str(s)
        for i,v in enumerate(s1):
            if v not in tmp:
                tmp[v]=dict()
            if i==len(s1)-1:
                tmp[v][self.END]=s1
            tmp=tmp[v]
    def query_max(self,v):
        s1=self.get_num_str(v)
        if not self.map:
            return -1
        ret=0
        tmp=self.map
        for i,v in enumerate(s1):
            aimv='1' if v=='0' else '0'
            if aimv in tmp:
                tmp=tmp[aimv]
                ret+=1<<(self.size-i-1)
            elif v in tmp:
                tmp=tmp[v]
            else:
                break
        return ret