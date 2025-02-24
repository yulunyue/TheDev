from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(expression = "2-1-1",result=[0,2]),
        ]
    def execute(self, expression: str) -> List[int]:
        op={"+":lambda a,b:a+b,"-":lambda a,b:a-b,"*":lambda a,b:a*b}
        ops=[]
        num=[]
        last_s=""
        for e in expression:
            if e in op:
                ops.append(e)
                num.append(int(last_s))
                last_s=""
            else:
                last_s+=e
        num.append(int(last_s))
        ans=dict()
        def dfs(os,ns):
            if not os:
                ans[ns[0]]=True
                return
            for i in range(len(os)):
                c=op[os[i]](ns[i],ns[i+1])
                dfs(os[:i]+os[i+1:],ns[:i]+[c]+ns[i+2:])
        # self.log([ops,num])
        dfs(ops,num)
        return list(ans.keys())
    def diffWaysToCompute(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
 



if __name__=='__main__':
    Solution().run()