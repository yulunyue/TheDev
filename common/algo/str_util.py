class Manacher:
    def __init__(self, s) -> None:
        self.s = s

    def get_odd_p(self):
        n = len(self.s)
        ret = [0]*n
        l, r = 0, -1
        for i in range(n):
            if i > r:
                k = 1
            else:
                k = min(ret[l+r-i], r-i+1)
            while k <= i and i+k < n and self.s[i-k] == self.s[i+k]:
                k += 1
            ret[i] = k
            k -= 1
            if i+k > r:
                l = i-k
                r = i+k
        return ret
