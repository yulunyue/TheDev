from common.util.export import MockCf, functools, List


@functools.lru_cache(None)
def find(e, b=1):
    if e < b:
        return []
    if e == b:
        return [[e]]
    ret = []
    for s in range(b, e + 1):
        for v in find(e - s, s + 1):
            ret.append([s] + v)
    return ret + [[e]]


class Solution(MockCf):
    def zero_one_ksack(self, a: List[int], target: int):
        pass

    def nextBeautifulNumber(self, n: int) -> int:
        s = [0] + [int(v) for v in str(n)]
        m = len(s)
        cnt = [0]
        # for i in range(1, m):
        #     cnt[s[i]] += 1
        for i in range(m - 1, -1, -1):
            # if i > 0:
            #     cnt[s[i]] -= 1
            for j in range(s[i] + 1, 10):
                # s[i] = j
                tail = [j]
                for k, c in enumerate(cnt):
                    if c < 0:
                        c = -c
                    else:
                        c = c + k
                    tail += [k] * c
                return int("".join(map(str, s[:i] + tail)))
        return -1

    def nextBeautifulNumber(self, n: int) -> int:
        s = [int(v) for v in str(n)]
        m = len(s)
        a = find(m)
        self.ans = None

        def check(cnt):
            is_limt = False
            for i, v in enumerate(n):
                pass
            min_value = []
            for v in cnt:
                min_value.extend([v] * v)
            max_value = min_value[:]
            max_value.reverse()
            if max_value <= s:
                return True
            if min_value > s:
                self.ans = min_value
                return False

            self.logger.map(cnt=cnt, min_value=min_value, max_value=max_value)

        for i in range(len(a) - 1, -1, -1):
            if check(a[i]):
                if self.ans is None:
                    return int("".join([str(v) * v for v in find(m)[0]]))
                return int("".join([str(v) for v in self.ans]))

    execute = nextBeautifulNumber
