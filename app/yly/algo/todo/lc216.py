from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/combination-sum-iii/'
    def get_cases(self):
        return [
            dict(k = 3, n = 7,result=[[1,2,4]])
        ]   
    
    def combinationSum3(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    
    def execute(self, k: int, n: int) -> List[List[int]]:
        ret=[]
        def dfs(i,a,b,m):
            if i==k:
                if m==n:
                    ret.append(a[:])
                return
            for j in range(b,10):
                if m+j>n:
                    continue
                dfs(i+1,a+[j],j+1,m+j)
           

        dfs(0,[],1,0)
        return ret



if __name__=='__main__':
    Solution().run()