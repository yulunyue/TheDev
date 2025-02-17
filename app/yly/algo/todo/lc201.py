from app.yly.algo.manage import SolutionBase,View,bisect,defaultdict,\
    Dict,List,MOD,inf,heapq
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/bitwise-and-of-numbers-range/submissions/600330795/'
    def get_cases(self):
        return [
            dict(left = 3, right = 3,result=3),
            dict(left = 5, right = 7,result=4),
            dict(left = 1, right = 2147483647,result=0),
            dict(left = 0, right = 0,result=0),
        ]
    
    def rangeBitwiseAnd(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
    def execute(self, left: int, right: int) -> int:
        if left==right:
            return left
        v=1
        c=right-left
        while v*2<=left:
            v*=2
        r=right&v
        ans=0
        while v:
            if v>=c and v&left and v&r:
                ans+=v
            v=v>>1
        return ans


if __name__=='__main__':
    Solution().run()