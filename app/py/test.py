class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        s = [ord(ch)-97 for ch in s]
        cnt = [0] * 26
        for x in s:
            cnt[x] += 1
        ans = inf
        for tar in range(1, n+1):
            dp = [[0, 0] for _ in range(27)]
            for i in range(26):
                if cnt[i] < tar:
                    dp[i+1][0] = dp[i][0] + min(cnt[i], tar - cnt[i])
                    if i > 0:
                        if cnt[i-1] < tar:
                            dp[i+1][0] = min(dp[i+1][0], dp[i][1] + max(0, tar-cnt[i]-cnt[i-1]))
                        else:
                            dp[i+1][0] = min(dp[i+1][0], dp[i][1] + max(0, tar*2-cnt[i]-cnt[i-1]))
                    dp[i+1][1] = dp[i][0] + cnt[i]
                else:
                    dp[i+1][0] = dp[i+1][1] = min(dp[i][0], dp[i][1]) + cnt[i] - tar
            ans = min(ans, dp[26][0], dp[26][1])
            if ans == 0:
                return 0
        return ans