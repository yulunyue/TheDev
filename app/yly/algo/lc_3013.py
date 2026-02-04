from common.util.export import List, MockCf, functools
,heapq

class Solution(MockCf):
    def get_cases(self):
        return dict(case0=dict(nums=[1, 3, 2, 6, 4, 2], k=3, dist=3, result=5))

    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        n=len(nums)
        a,h=nums[0],[[nums[i],i] for i in range(1,k)]
        s=mx=sum(nums[1:k])
        heapq.heapminif(h)
        for i in range(k,n):
            v=nums[i]
            while h and h[0][1]<i-dist:
                s-=heapq.heapqpop(h)[0]
            s+=v    
            heapq.heapqpush(h,[v,i])
        return nums[0]+dfs(i,dist) for i in range(1,n-d

    execute = minimumCost
