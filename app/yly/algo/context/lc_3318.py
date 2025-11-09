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
            append(fv1, sl)
            while len(sr) < x and sl:
                fv1 = sl.pop()
                append(fv1, sr)
                self.s += fv1[1] * fv1[0]

            if sl and sl[-1] > sr[0]:
                fv2, fv3 = sr.pop(0), sl.pop()
                sr.add(fv3)
                sl.add(fv2)
                self.s += fv3[1] * fv3[0] - fv2[1] * fv2[0]

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

    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:
        cnt = defaultdict(int)
        L = SortedList()  # 保存 tuple (出现次数，元素值)
        R = SortedList()
        sum_l = 0  # L 的元素和

        def add(val: int) -> None:
            if cnt[val] == 0:
                return
            p = (cnt[val], val)
            if L and p > L[0]:  # p 比 L 中最小的还大
                nonlocal sum_l
                sum_l += p[0] * p[1]
                L.add(p)
            else:
                R.add(p)

        def remove(val: int) -> None:
            if cnt[val] == 0:
                return
            p = (cnt[val], val)
            if p in L:
                nonlocal sum_l
                sum_l -= p[0] * p[1]
                L.remove(p)
            else:
                R.remove(p)

        def l2r() -> None:
            nonlocal sum_l
            p = L[0]
            sum_l -= p[0] * p[1]
            L.remove(p)
            R.add(p)

        def r2l() -> None:
            nonlocal sum_l
            p = R[-1]
            sum_l += p[0] * p[1]
            R.remove(p)
            L.add(p)

        ans = [0] * (len(nums) - k + 1)
        for r, in_ in enumerate(nums):
            # 添加 in_
            remove(in_)
            cnt[in_] += 1
            add(in_)

            l = r + 1 - k
            if l < 0:
                continue

            # 维护大小
            while R and len(L) < x:
                r2l()
            while len(L) > x:
                l2r()
            ans[l] = sum_l

            # 移除 out
            out = nums[l]
            remove(out)
            cnt[out] -= 1
            add(out)
        return ans

    execute = findXSum
