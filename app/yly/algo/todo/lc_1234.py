from collections import Counter


class Solution:
    def balancedString(self, s: str) -> int:
        n = len(s)
        target = n // 4
        total = Counter(s)

        if all(cnt == target for cnt in total.values()):
            return 0

        ans = n
        l = 0
        win = Counter()

        for r, ch in enumerate(s):
            win[ch] += 1

            while all(total[c] - win[c] <= target for c in "QWER"):
                ans = min(ans, r - l + 1)
                win[s[l]] -= 1
                l += 1

        return ans