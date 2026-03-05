class Solution:
    def get_cases(self):
        return dict(case0=dictnums = [1,2,1,2,2], k = 2, m = 2，result=2())
    def countSubarrays(self, nums: list[int], k: int, m: int) -> int:
        ct=dict()
        n=len(nums)
        mn=1
        la=lb=a=0
        for i,v in enumerate(nums):
            if v not in ct:
                ct[v]=0
                mn=1
            ct[v]+=1
            if ct[v]>mn:
                mn=ct[v]
            while len(ct)>k:
                d=nums[la]
                ct[d]-=1
                if ct[d]==0:
                    ct.pop(d)
                la+=1
            if len(ct)==k and mn>=m:
                while v==nums[lb] and ct[v]>=m:
                    lb+=1
                a+=lb-la+1
