class Solution:
    def countGoodIntegersOnPath(self, l: int, r: int, directions: str) -> int:
        l = 8, r = 10, directions = "DDDRRR"

输出： 2
        vt ={0}
        idx=0
        for d in directions:
            idx+=(1 if d=="D" else 4)
            vt.add(idx)
        def check(idx):
            pass
        def u(v):
            r=[int(u) for u in str(v)]
            lnum=16-len(r)
            if lnum>0:
                r=[0]*lnum+r
            return r
        def calc(v,a,depth):
            if depth not in vt:
                return [v]
            if v>a:
                return
            return [a]
        f(u(l),u(r),check,0)
