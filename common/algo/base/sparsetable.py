import functools


class SparseTable:
    def __init__(self, data):
        self.n = len(data)
        self.data = data

    def query_cache_max(self, lidx, ridx):
        if lidx > ridx or ridx >= self.n:
            raise Exception(lidx, ridx, self.data)

        @functools.lru_cache(None)
        def q(l, r):
            if l == r:
                return self.data[l]
            m = (l + r) // 2
            lv = q(l, m)
            rv = q(m + 1, r)
            return rv if lv < rv else lv

        return q(lidx, ridx)
