from common.util.export import MockCf, List
from common.algo.base.segtree import SegTreeNode


class T(SegTreeNode):
    def load(self, s):
        self.value = [s[self.l], 1, s[self.l]]

    def do(self, v):
        self.value = [v, 1, v]

    def merge(self, lv, rv):
        ll, lc, lr = lv
        rl, rc, rr = rv
        c = lc + rc
        if lr == rl:
            c -= 1
        return [ll, c, rr]


class Solution(MockCf):
    """
    给定一个只有AB的数组M，和一个操作序列Q，Q有两钟操作
    操作一翻转i M[i]='A' if M[i]=='B' else 'A'
    操作二查询i，j 求至少需要删除多少个元素使得M[i:j+1]为AB交替，删除不改变原数组
    返回每个操作二的结果
    区间需要删除多少个元素 = 区间里的长度-区间里的来纳许段的数量
    """

    def get_cases(self):
        return dict(
            case0=dict(s="ABA", queries=[[2, 1, 2], [1, 1], [2, 0, 2]], result=[0, 2]),
        )

    def minDeletions(self, s: str, queries: List[List[int]]) -> List[int]:
        s = list(s)
        t = T().set_range(0, len(s) - 1)
        t.build(s)
        ans = []
        # self.logger.info(t)
        for tp, *args in queries:
            if tp == 1:
                c = "B" if s[args[0]] == "A" else "A"
                t.update(args[0], args[0], c)
                s[args[0]] = c
            else:
                ans.append(args[1] - args[0] + 1 - t.query(args[0], args[1])[1])
        return ans

    execute = minDeletions


if __name__ == "__main__":
    Solution().run()
