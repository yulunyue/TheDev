from typing import List
class TieNode:
    def __init__(self,size,length=0) -> None:        
        self.size=size
        self.childs:List[TieNode]=[None]*size
        self.fail:TieNode = None
        self.length=length
    def add(self,s):
        tmp=self
        for i in s:
            if tmp.childs[i] is None:
                tmp.childs[i]=TieNode(self.size,tmp.length+1)
            tmp=tmp.childs[i]
    def build_fail(self):
        self.fail=self
        q:List[TieNode]=[]
        for i in range(self.size):
            if self.childs[i] is None:
                self.childs[i]=self
            else:
                self.childs[i].fail=self
                q.append(self.childs[i])
        while q:
            cur=q.pop(0)
            for k,son in enumerate(cur.childs):
                if son is None:
                    cur.childs[k]=cur.fail.childs[k]
                    continue
                son.fail = cur.fail.childs[k]
                q.append(son)


    def get_num_str(self, s: int):
        ss = bin(s)[2:]
        s1 = '0'*(self.size-len(ss))+ss
        return s1

    def add(self, s: int):
        tmp = self.map
        s1 = self.get_num_str(s)
        for i, v in enumerate(s1):
            if v not in tmp:
                tmp[v] = dict()
            if i == len(s1)-1:
                tmp[v][self.END] = s1
            tmp = tmp[v]

    def query_max(self, v):
        s1 = self.get_num_str(v)
        if not self.map:
            return -1
        ret = 0
        tmp = self.map
        for i, v in enumerate(s1):
            aimv = '1' if v == '0' else '0'
            if aimv in tmp:
                tmp = tmp[aimv]
                ret += 1 << (self.size-i-1)
            elif v in tmp:
                tmp = tmp[v]
            else:
                break
        return ret
