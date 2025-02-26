from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools
class Solution(SolutionBase):
    uri='https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-ii/description/'
    def get_cases(self):
        return [
            dict( s = "3902",result=True),
            dict(s='34789',result=False)
        ]
    def execute(self, s: str) -> bool:
        s=[int(v) for v in s]
        a,b=s[0],s[1]
        c=d=1
        for i in range(2,len(s)):
            c*=(i-1)
            d*=(len(s)-i)
            a=(a+s[i-1]*d//c)%10
            b=(b+s[i]*d//c)%10
        #     self.log([a,b,c,d])
        # self.log([a,b])
        return a==b
    def hasSameDigits(self,*args,**kw):
        self.init(*args,**kw)
        return self.execute(*args,**kw)
        




if __name__=='__main__':
    Solution().run()