from common.mock import MockBase, IoTxtFile
from common.util.export import logger, heapq, defaultdict


class Solution(MockBase):
    yawn_path = "0710"

    def __init__(self):
        super().__init__()
        self.io = IoTxtFile()

    def main(self):

        n, *args = self.io.ii()
        ans = []
        area = []
        for _ in range(n):
            y, l, r = self.io.ii()
            area.append([l, y, 1])
            area.append([r, y, -1])
        area.sort()
        lazy_remove = dict()
        hq = [0]
        for x, y, tp in area:
            if tp == 1:
                if hq and y > -hq[0]:
                    ans.append(f"{x} {-hq[0]}")
                    ans.append(f"{x} {y}")
                heapq.heappush(hq, -y)
                lazy_remove[y] = lazy_remove.get(y, 0) + 1
            if tp == -1:
                lazy_remove[y] = lazy_remove.get(y, 0) - 1
                if hq and -hq[0] == y:
                    ans.append(f"{x} {y}")
                    while hq and lazy_remove.get(-hq[0]) == 0:
                        heapq.heappop(hq)
                    ans.append(f"{x} {-hq[0]}")
        return ans


if __name__ == "__main__":
    Solution().run()
