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


 