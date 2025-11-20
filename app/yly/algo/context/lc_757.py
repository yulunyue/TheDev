from common.util.export import List, MockCf, bisect


class Solution(MockCf):
    """
    线段树todo
    """

    def intersectionSizeTwo(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: (x[1], -x[0]))

        ans = 2  # 第一个区间需要
        end = intervals[0][1]
        pre_end = end - 1  # 贪心地将pre_end设置为end-1

        for x, y in intervals[1:]:

            if x <= pre_end:  # x <= pre_end < end <= y【无需添加元素】
                continue

            if x <= end:  # pre_end < x <= end <= y【只需添加y为end】
                ans += 1
                pre_end = end
                end = y
            else:  # end < x < y【需添加y为end，y-1为pre_end】
                ans += 2
                pre_end = y - 1  # 贪心地将pre_end设置为y-1
                end = y

        return ans

    def intersectionSizeTwo(self, intervals: List[List[int]]) -> int:
        intervals = sorted(intervals, key=lambda v: v[1])
        st = [(-2, -2, 0)]
        for start, end in intervals:
            idx = bisect.bisect_left(st, (start,)) - 1
            _, r, s = st[idx]
            d = 2 - (st[-1][2] - s)
            if start <= r:
                d -= r - start + 1
            if d <= 0:
                continue
            while end - st[-1][1] <= d:
                l, r, _ = st.pop()
                d += r - l + 1
            st.append((end - d + 1, end, st[-1][2] + d))
            self.logger.map(start=start, end=end, d=d, st=st)
        return st[-1][2]

    execute = intersectionSizeTwo
