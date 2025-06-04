from common.algo.base.str_util import manacher_get_odd_p


class Solution:
    """
    https://leetcode.cn/problems/longest-palindrome-after-substring-concatenation-ii/
    """

    def get_cases(self):
        return [dict(s="abcde", t="ecdba", result=5)]

    def longestPalindrome(self, s: str, t: str) -> int:
        s1 = manacher_get_odd_p(s)
        t1 = manacher_get_odd_p(t)
        mn = max(s1 + t1) * 2 + 1
        return
