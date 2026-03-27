from common.util.export import MockCf, List, functools


class Solution(MockCf):
    """
    给定一个子数组，求子数组的或为子数组的最大值的数量
    随着子数组右端点向右移动，子数组的最大值
    每一位递归找之前的0
    """

    def get_cases(self):
        return dict(
            case1=dict(nums=[1, 2, 3], result=5),
            case3=dict(nums=[1, 3, 1], result=6),
            case0=dict(nums=[6, 10, 4], result=3),
        )

    def countGoodSubarrays(self, nums: list[int]) -> int:
        n = len(nums)
        mx = max(nums)
        mx_or = (1 << mx.bit_length()) - 1

        @functools.lru_cache(None)
        def dfs(i, v,  max_exist):
            if i < 0:
                return 0
            if nums[i] == mx_or:
                return i + 1
            v_or = nums[i] | v
            if v_or == v or v_or == nums[i]:
                max_exist = max_exist or v_or == nums[i]
                return  max_exist+ dfs(i - 1, v_or,max_exist)
            r = dfs(i - 1, v_or, False)
            return r

        suf=[0]*(n+1)
        for i in range(n-1,-1-1):
            suf[i]=suf[i+1]|nums[i]
        s,ev=0,[0,0]
        for i,v in enumerate(nums):
            if v==mx_or:
                ev=[i+1,i+1]
            elif suf[i]==suf[i+1] or suf[i]==nums[i]:
                for ei in range(2):
                    nei=ei or suf[i]==nums[i]
                    ev[ei]=nei+ev[nei]
                    
            else:
                ev[1]=ev[0]
            s+=ev[1]
        return s

    execute = countGoodSubarrays
