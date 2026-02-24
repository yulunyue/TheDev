from common.util.export import List,defaultdict
from common.algo.base.comb import Comb

MX = 20
C = Comb().load(MX)
F=dict()
for i in range(2, MX):
    for k in range(1,i+1):
        for j in range(i-k+1):
            F[i,k]+=C.comb(i,j+k)*C.comb(i-j-k,j)


class Solution:
    def get_cases(self):
        return dict(dict(nums=[2, 3, 2], k=6, result=2))

    def countSequences(self, nums: List[int], k: int) -> int:
        ct = [0] * 6
        a1 = 1
        kt=[0]*6
        for v in nums:
            if v == 1:
                a1 *= 3
                continue
            elif k % v == 0:
                k = k // v
                kt[v]+=1
            ct[v] += 1
        kt[2]+=2*kt[4]
        if k != 1:
            return 0
        a35=F[ct[3],kt[3]]*F[ct[5],kt[5]]
        return a1*a35

    execute = countSequences
