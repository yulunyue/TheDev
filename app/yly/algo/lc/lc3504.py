from common.algo.base.str_util import manacher_get_odd_p, get_height_form_sa
from common.util.export import logger


class Solution:
    """
    https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-ii/
    """

    def get_cases(self):
        return [dict(s="abcde", t="ecdba", result=5), dict(s="a", t="a", result=2)]

    def longestPalindrome(self, s: str, t: str) -> int:

        def util(u, v):
            n = len(u)
            us = manacher_get_odd_p(u)
            sv = u + "#" + v[::-1]
            h, sa, rk = get_height_form_sa(sv)
            logger.pt(f"\ns:{sv}\nh2:{h}\nsa:{sa}\nrk:{rk}")
            logger.pt(us)
            hi = [0] * len(u)
            for i in range(1, len(h)):
                a, b = sa[i - 1], sa[i]
                if v == 0 or (a - n) * (n - b) <= 0:
                    continue
                k = min(a, b) + h[i] - 1
                logger.pt([a, b, k])
                hi[k] = max(hi[k], h[i])
            logger.pt(hi)
            ans = 0
            for i in enumerate(1, range(len(us)), 2):
                ans = max(2 * v + 1 + hi[i] * 2, ans)
            return ans

        return max(util(s, t), util(t[::-1], s[::-1]))
