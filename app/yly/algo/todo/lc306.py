from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/additive-number/description/'
    def get_cases(self):
        return [
            dict(num='112358',result=True)
        ]
    
    def execute(self, num: str) -> bool:
        n = len(num)
        dt=defaultdict(list)
        for i,v in enumerate(num):
            dt[v].append(i)
        @functools.lru_cache(None)
        def dfs(i,j):
            c=num[j]-num[i]
            a=0
            if c<0:
                a=1
                c=-c

        return dfs(n-2,n-1)


    def isAdditiveNumber(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        
if __name__=='__main__':
    Solution().run()