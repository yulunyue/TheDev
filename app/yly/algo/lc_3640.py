from common.util.export import List, MockCf


class Solution(MockCf):
    def get_cases(self):
        return dict(
            case0=dict(nums=[0, -2, -1, -3, 0, 2, -1], result=-4),
            case1=dict(nums=[1,4,2,7],result= 14)
        )

    def maxSumTrionic(self, nums: List[int]) -> int:
        n=len(nums)
        l1=l2=ml=None
        self.logger.info(nums)
        mx=float("-inf")
        lc=0
        for i in range(1,n):
            u,v=nums[i-1],nums[i]
            c=v-u
            if c==0:
                l1=l2=ml=None
            if c>0:
                if l1 is None:
                    l1=u
                if ml is None or lc<0:
                    ml=u
                l1+=v
                if l2 is not None:
                    mx=max(mx,l2+l1)
                ml=max(ml,v,l1)
            if c<0:
                if ml is not None:
                    l2=v+ml 
                l1=0
            lc=c
            self.logger.map(u=u,v=v,l1=l1,l2=l2,ml=ml,mx=mx)
        return mx

    execute = maxSumTrionic
