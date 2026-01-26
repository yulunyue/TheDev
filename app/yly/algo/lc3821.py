from common.algo.base.math_util import Comb
class Solution:
    def get_cases(self):
        return dict(case0=dict(n=4,k=2,result=9))
    def nthSmallest(self, n: int, k: int) -> int:
        a=0
        cm=Comb()
        def c(i,j,n):
            return cm.comb(i+1,j)<=n
        for j in range(k,0,-1):
            m=bisect.bisect_right(range(0,52),False,lambda i:c(i,j,n)-1
            n-=cm.comb(m+1,k)
            a|=1<<m
