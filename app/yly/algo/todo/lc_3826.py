from common.util.export import MockCf


class Solution(MockCf):
    """
    将一个长度为为n的正整数数组A，恰好分成连续的k个子数组，如何求k个子数组和的平方的和的最小值
    a[i][j]=min(a[t][j-1]+(p[i]-p[t])**2,j-1<=t<=i)
        =p[i]**2+min(a[t][j-1]+p[t]**2 -2*p[i] *p[t])
    """

    def get_cases(self):
        return dict(
            case0=dict(nums=[1, 1, 1], k=3, result=3),
            case1=dict(nums=[1, 1, 1], k=2, result=1),
        )

    def minPartitionScore(self, nums: List[int], k: int) -> int:
        n=len(nums)
        p=[0]*(n+1)
        for i,v in enumerate(nums):
            p[i+1]=p[i]+v
        for j in range(k):
            q=S()
            for i in range(n):
                x=p[i+1]
                y=p[i+1]**2
                if j>0:
                    y*


    execute = minPartitionScore
