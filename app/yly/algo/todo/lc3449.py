from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(points = [2,4], m = 3,result=4),
        ]
    def execute(self, points: List[int], m: int) -> int:
        pass
    def maxScore(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        




if __name__=='__main__':
    Solution().run()