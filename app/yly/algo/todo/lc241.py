from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(expression = "2-1-1",result=[2,0]),
            dict(expression="2*3-4*5",result=[-34,-10,-14,-10,10]),
        ]
    def execute(self, expression: str) -> List[int]:
        op={"+":lambda a,b:a+b,"-":lambda a,b:a-b,"*":lambda a,b:a*b}
        @functools.lru_cache(None)
        def dfs(ep:str):
            if ep.isdecimal():
                return [int(ep)]
            ans = []
            for i,v in enumerate(ep):
                if v not in op:
                    continue
                left,right=dfs(ep[:i]),dfs(ep[i+1:])
                for l in left:
                    for r in right:
                        ans.append(op[v](l,r))
            return ans
        return dfs(expression)
        
    def diffWaysToCompute(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
 



if __name__=='__main__':
    Solution().run()