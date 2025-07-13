import heapq
from collections import defaultdict


class Solution:

    def run(self):
        inputs=open("input.txt","r").read()
        ins=inputs.split("\n")
        n=int(ins.pop(0))
        wt=open("output.txt","w")
        ans = []
        area = defaultdict(lambda:[0,0])
        for _ in range(n):
            y, l, r = self.io.ii()
            area[l][0]=max(area[l][0],y)
            area[r][1]=max(area[r][1],y)
        keys=sorted(area)
        hq = [0]
        for x in keys:
            y=area[x][0]
            if y:
                if hq and y > -hq[0]:
                    ans.append(f"{x} {-hq[0]}")
                    ans.append(f"{x} {y}")
                heapq.heappush(hq, -y)
            y=area[x][1]
            if y:
                if hq and -hq[0] == y:
                    wt.write(f"{x} {y}")
                    heapq.heappop(hq)
                    wt.write(f"{x} {-hq[0]}")
        wt.flush()


if __name__ == "__main__":
    Solution().run()
