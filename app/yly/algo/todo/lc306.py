from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(num="112358",result=True),
            dict(num="199100199",result=True)
        ]
    def execute(self, num: str) -> bool:
        num=[int(v) for v in num]
        n=len(num)

        def calc(l:list,r:list):
            x=0
            ret=[]
            while l or r:
                c=(l.pop() if l else 0)+(r.pop() if r else 0)+x
                x=1 if c>=10 else 0
                ret.insert(0,c%10)
            if x:
                ret.insert(0,x)
            return ret

        def dfs1(i,j):
            i1,i2,i3=0,i,j
            while i3<len(num):
                s=calc(num[i1:i2],num[i2:i3])
                if (num[i1]==0 and i2>i1+1) or (num[i2]==0 and i3>i2+1):
                    return False
                if s!=num[i3:i3+len(s)]:
                    return False
                # self.log(num[i1:i2],num[i2:i3],s)
                i1,i2,i3=i2,i3,i3+len(s)
            return True
                
        for i in range(1,n):
            for j in range(i+1,n):
                if dfs1(i,j):
                    return True
        return False

    def isAdditiveNumber(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
  



if __name__=='__main__':
    Solution().run()