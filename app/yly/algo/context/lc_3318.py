from common.util.export import MockCf,List,defaultdict
from common.third_util.sort import SortedList
class Solution(MockCf):
    def findXSum(self, nums:List[int],k:int,x:int):
        sl,sr=SortedList(),SortedList()
        ct=defaultdict(int)
        self.s=0
        def f(v):
            return [ct[v],v]
        def rv(fl,v):
            if v in fl:
                fl.remove(v)
                return True
        def add(v):
            if ct[v]:
                if rv(sl,f(v)):
                    self.s-=v*ct[v]
                rv(sr,f(v))
            ct[v]+=1
            if len(sr)<x:
                sr.add(f(v))
                self.s+=v*ct[v]
            elif sr[0]<f(v):
                rr=sr.pop(0)
                sl.add(sr.pop(0))
                sr.add(f(v))
                self.s+=

        for i,v in enumerate(nums):
            add(v)
            self.logger.map(v=v,sl=sl,sr=sr,s=self.s)


    execute=findXSum
    


