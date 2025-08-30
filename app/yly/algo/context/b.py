from common.util.export import List, defaultdict, Dict, bisect, logger


class Solution:
    def get_cases(self):
        return [
            dict(cards=["bb", "ba"], x="b", result=1),
            dict(
                cards=[
                    "ab",
                    "aa",
                    "ab",
                    "bc",
                    "cc",
                    "bc",
                    "bb",
                    "ac",
                    "bc",
                    "bc",
                    "aa",
                    "aa",
                    "ba",
                    "bc",
                    "cb",
                    "ba",
                    "ac",
                    "bb",
                    "cb",
                    "ac",
                    "cb",
                    "cb",
                    "ba",
                    "bc",
                    "ca",
                    "ba",
                    "bb",
                    "cc",
                    "cc",
                    "ca",
                    "ab",
                    "bb",
                    "bc",
                    "ba",
                    "ac",
                    "bc",
                    "ac",
                    "ac",
                    "bc",
                    "bb",
                    "bc",
                    "ac",
                    "bc",
                    "aa",
                    "ba",
                    "cc",
                    "ac",
                    "bb",
                    "ba",
                    "bb",
                ],
                x="b",
                result=16,
            ),
            dict(cards=["aa", "ab", "aa", "ba"], x="a", result=2),
            dict(cards=["ba", "ba"], x="b", result=0),
            dict(cards=["ab", "bb"], x="b", result=1),
            dict(cards=["bb", "bb"], x="b", result=0),
            dict(cards=["aa", "ab", "ba", "ac"], x="a", result=2),
        ]

    def score(self, cards: List[str], x: str) -> int:
        ct0s = ct1s = c0 = 0
        ct0m = ct1m = 0
        ct = defaultdict(int)
        for c in cards:
            if c[0] == c[1] == x:
                c0 += 1
            elif c[0] == x:
                ct0s += 1
                ct[0, c[1]] += 1
                ct0m = max(ct0m, ct[0, c[1]])
            elif c[1] == x:
                ct1s += 1
                ct[1, c[0]] += 1
                ct1m = max(ct1m, ct[1, c[0]])

        def u(s, m):
            return min(s // 2, s - m)

        # logger.map()
        ans = u(ct0s, ct0m) + u(ct1s, ct1m)
        for l in range(c0 + 1):
            r = c0 - l
            ans = max(ans, u(ct0s + l, max(ct0m, l)) + u(ct1s + r, max(ct1m, r)))
        return ans

    def execute(self, *args, **kw):
        return self.score(*args, **kw)
