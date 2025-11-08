from common.util.export import MockCf, List, defaultdict
from common.third_util.sort import SortedList


class Solution(MockCf):
    def findXSum(self, nums: List[int], k: int, x: int):
        sl, sr = SortedList(), SortedList()
        ct = defaultdict(int)
        self.s = 0

        def rv(v, fl):
            if v in fl:
                fl.remove(v)
                return True

        def append(v, fl):
            if v[0]:
                fl.add(v)
                return True

        def add(v, u):
            fv0, fv1 = (ct[v], v), (ct[v] + u, v)
            ct[v] += u
            rv(fv0, sl)
            if rv(fv0, sr):
                self.s -= fv0[1] * fv0[0]
            if append(fv1, sl):
                fv2 = sl.pop()
                append(fv2, sr)
                self.s += fv2[1] * fv2[0]
            if len(sr) > x:
                fv3 = sr.pop(0)
                append(fv3, sl)
                self.s -= fv3[1] * fv3[0]

        ans = []
        for i, v in enumerate(nums):
            add(v, 1)
            self.logger.map(
                v=v,
                s=self.s,
                sl=list(sl),
                sr=list(sr),
            )
            if i >= k - 1:
                ans.append(self.s)
                add(nums[i - k + 1], -1)

        return ans

    execute = findXSum
