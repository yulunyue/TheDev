standard_input, packages, output_together = 1, 1, 1
dfs, hashing, read_from_file = 1, 0, 0
de = 1
if 1:
    if standard_input:
        import io, os, sys
        input = lambda: sys.stdin.readline().strip()
 
        import math
        inf = math.inf
 
        def I():
            return input()
        
        def II():
            return int(input())
 
        def MII():
            return map(int, input().split())
 
        def LI():
            return list(input().split())
 
        def LII():
            return list(map(int, input().split()))
 
        def LFI():
            return list(map(float, input().split()))
 
        def GMI():
            return map(lambda x: int(x) - 1, input().split())
 
        def LGMI():
            return list(map(lambda x: int(x) - 1, input().split()))
 
    if packages:
        from io import BytesIO, IOBase
 
        import random
        import os
 
        import bisect
        import typing
        from collections import Counter, defaultdict, deque
        from copy import deepcopy
        from functools import cmp_to_key, lru_cache, reduce
        from heapq import merge, heapify, heappop, heappush, heappushpop, nlargest, nsmallest
        from itertools import accumulate, combinations, permutations, count, product
        from operator import add, iand, ior, itemgetter, mul, xor
        from string import ascii_lowercase, ascii_uppercase, ascii_letters
        from typing import *
        BUFSIZE = 4096
 
    if output_together:
        class FastIO(IOBase):
            newlines = 0
 
            def __init__(self, file):
                self._fd = file.fileno()
                self.buffer = BytesIO()
                self.writable = "x" in file.mode or "r" not in file.mode
                self.write = self.buffer.write if self.writable else None
 
            def read(self):
                while True:
                    b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
                    if not b:
                        break
                    ptr = self.buffer.tell()
                    self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
                self.newlines = 0
                return self.buffer.read()
 
            def readline(self):
                while self.newlines == 0:
                    b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
                    self.newlines = b.count(b"\n") + (not b)
                    ptr = self.buffer.tell()
                    self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
                self.newlines -= 1
                return self.buffer.readline()
 
            def flush(self):
                if self.writable:
                    os.write(self._fd, self.buffer.getvalue())
                    self.buffer.truncate(0), self.buffer.seek(0)
 
        class IOWrapper(IOBase):
            def __init__(self, file):
                self.buffer = FastIO(file)
                self.flush = self.buffer.flush
                self.writable = self.buffer.writable
                self.write = lambda s: self.buffer.write(s.encode("ascii"))
                self.read = lambda: self.buffer.read().decode("ascii")
                self.readline = lambda: self.buffer.readline().decode("ascii")
 
        sys.stdout = IOWrapper(sys.stdout)
 
    if dfs:
        from types import GeneratorType
 
        def bootstrap(f, stk=[]):
            def wrappedfunc(*args, **kwargs):
                if stk:
                    return f(*args, **kwargs)
                else:
                    to = f(*args, **kwargs)
                    while True:
                        if type(to) is GeneratorType:
                            stk.append(to)
                            to = next(to)
                        else:
                            stk.pop()
                            if not stk:
                                break
                            to = stk[-1].send(to)
                    return to
            return wrappedfunc
 
    if hashing:
        RANDOM = random.getrandbits(20)
        class Wrapper(int):
            def __init__(self, x):
                int.__init__(x)
 
            def __hash__(self):
                return super(Wrapper, self).__hash__() ^ RANDOM
 
    if read_from_file:
        file = open("input.txt", "r", encoding='utf-16').readline().strip()
        fin = open(file, 'r')
        input = lambda: fin.readline().strip()
        output_file = open("output.txt", "w")
        def fprint(*args, **kwargs):
            print(*args, **kwargs, file=output_file)
 
    if de:
        def debug(*args, **kwargs):
            print('\033[92m', end='')
            print(*args, **kwargs)
            print('\033[0m', end='')
 
    fmax = lambda x, y: x if x > y else y
    fmin = lambda x, y: x if x < y else y
 
    class lst_lst:
        def __init__(self, n) -> None:
            self.n = n
            self.pre = []
            self.cur = []
            self.lst = [-1] * n
        
        def append(self, i, j):
            self.pre.append(self.lst[i])
            self.lst[i] = len(self.cur)
            self.cur.append(j)
        
        def iterate(self, i):
            tmp = self.lst[i]
            while tmp != -1:
                yield self.cur[tmp]
                tmp = self.pre[tmp]
 
mod = 10 ** 9 + 7
 
class UnionFind:
    def __init__(self, n):
        self.parent_or_size = [-1] * n
        self.depth = [0] * n
 
    def find(self, a):
        acopy = a
        v = 0
        while self.parent_or_size[a] >= 0:
            v += self.depth[a]
            if v >= mod: v -= mod
            
            a = self.parent_or_size[a]
        
        while acopy != a:
            self.depth[acopy], v = v, v - self.depth[acopy]
            if v < 0: v += mod
            self.parent_or_size[acopy], acopy = a, self.parent_or_size[acopy]
        return a
 
    def merge(self, a, b, w):
        pa, pb = self.find(a), self.find(b)
        va, vb = self.getDepth(a), self.getDepth(b)
        
        w += va
        if w >= mod: w -= mod
        w -= vb
        if w < 0: w += mod
        
        self.parent_or_size[pa] += self.parent_or_size[pb]
        self.parent_or_size[pb] = pa
        self.depth[pb] = w
        
        return True
 
    def getDepth(self, a):
        self.find(a)
        return self.depth[a]

if __name__ == '__main__':
    n = II()
    dsu = UnionFind(n)
    ans = 0
    
    for i in range(n):
        tmp = LII()
        for j in range(1, len(tmp), 2):
            idx = tmp[j] - 1
            val = tmp[j + 1]
            if val < 0: val += mod
            
            val += dsu.getDepth(idx)
            if val >= mod: val -= mod
            
            ans += val
            if ans >= mod: ans -= mod
            
            u = dsu.find(idx)
            dsu.merge(i, u, val)
    
    print(ans)