from common.util.export import MockCf, functools

F = [[0] * 10]
G = [[0] * 10]

MAXN = 20

p10k = 1
for k in range(1, MAXN):
    g = G[-1][:]
    f = F[-1][:]
    s = sum(f)
    for d in range(10):
        s -= f[d]
        g[d] += s
        s += f[9 - d]
    for d in range(10):
        f[d] = g[d] + d * p10k
    F.append(f)
    G.append(g)
    p10k *= 10


free = [0]

for k in range(1, MAXN):
    free.append(free[-1] + sum(G[k - 1][1:]))


class Solution(MockCf):
    """
    Docstring for Solution
    给定一个闭区间 [n1, n2]
    求所有n, n1<=n<=n2 波峰波谷数量和
    """

    def totalWaviness(self, num1: int, num2: int) -> int:
        n1 = list(map(int, str(num1)))
        n2 = list(map(int, str(num2)))
        n = len(n2)
        diff_lh = n - len(n1)
        n1 = [0] * diff_lh + n1

        @functools.lru_cache(None)
        def dfs(i, last_cmp, last_digit, limit_low, limit_high):
            if i == n:
                return 0, 1
            lo = n1[i] if limit_low else 0
            hi = n2[i] if limit_high else 9
            waviness_sum = num_cnt = 0
            is_num = not limit_low or i > diff_lh
            for d in range(lo, hi + 1):
                c = (d > last_digit) - (d < last_digit) if is_num else 0
                sub1, sub2 = dfs(
                    i + 1, c, d, limit_low and d == lo, limit_high and d == hi
                )
                waviness_sum += sub1
                num_cnt += sub2
                if c * last_cmp < 0:
                    waviness_sum += sub2
            return waviness_sum, num_cnt

        return dfs(0, 0, 0, True, True)[0]

    def totalWaviness(self, num1: int, num2: int) -> int:
        def total(x):
            digits = [int(d) for d in str(x)]
            current = 0
            ans = 0
            p10 = 1
            for i in range(len(digits) - 1, -1, -1):
                d = digits[i]
                for d2 in range(i == 0, d):
                    if i > 0 and d2 < digits[i - 1]:
                        ans += F[len(digits) - i - 1][9 - d2]
                    elif i > 0 and d2 > digits[i - 1]:
                        ans += F[len(digits) - i - 1][d2]
                    else:
                        ans += G[len(digits) - i - 1][d2]
                if i > 0 and i + 1 < len(digits):
                    if d > digits[i - 1]:
                        ans += min(d * p10 // 10, current)
                    elif d < digits[i - 1]:
                        ans += max(current - (d + 1) * p10 // 10, 0)
                current += d * p10
                p10 *= 10
            ans += free[len(digits) - 1]
            return ans

        return total(num2 + 1) - total(num1)

    execute = totalWaviness
