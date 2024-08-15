from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from sortedcontainers import SortedList
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")
null = None
true = True
false = False
M = 10**9 + 7


class Solution:
    def get_cases(self):
        return [
            dict(pieces=["bishop", "rook"],
                 positions=[[8, 5], [7, 7]], result=96.1),
            dict(pieces=["queen"], positions=[[1, 1]], result=22),
            dict(pieces=["rook"], positions=[[1, 1]], result=15),
            dict(pieces=["queen", "bishop"], positions=[
                 [5, 7], [3, 4]], result=281)
        ]

    def countCombinations(self, pieces: List[str], positions: List[List[int]]) -> int:
        n = len(pieces)
        drs = dict(
            rook=[[0, 0], [0, 1], [0, -1], [-1, 0], [1, 0]],
            queen=[[0, 0], [0, 1], [0, -1], [-1, 0], [1, 0],
                   [-1, -1], [-1, 1], [1, -1], [1, 1]],
            bishop=[[0, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]],
        )
        vt_flag = [[0]*8 for _ in range(73)]

        def dfs(i, stacks):
            if i == n:
                self.log(stacks)
                return 1
            ret = 0
            y, x = positions[i]
            for dy, dx in drs[pieces[i]]:
                steps = (0, 1) if dy == 0 and dx == 0 else (1, 8)
                for k in range(*steps):
                    y1, x1 = y+dy*k, x+dx*k
                    if y1 < 1 or x1 < 1 or y1 > 8 or x1 > 8:
                        break
                    pos = y1*8+x1
                    if vt_flag[pos][k]:
                        break

                    for j in range(8):
                        vt_flag[pos][j] = 1
                    ret += dfs(i+1, stacks+[i, y1, x1])
                    # self.log(pieces[i], y1, x1, k, ret)
                    for j in range(8):
                        vt_flag[pos][j] = 0
            return ret
        return dfs(0, [])

    def test1(self, pieces: List[str], positions: List[List[int]]) -> int:
        def dfs(idx, stacks):  # 棋子下标
            if idx == l:  # 如果所有棋子都已落子，此方案可行，返回1
                self.log(stacks)
                return 1
            i, j = positions[idx]  # 棋子的初始位置
            res = 0
            # 如果棋子当前位置上所有时间状态位都不存在棋子才可以落子，否则会相遇。
            if all(visit[i][j][k] == 0 for k in range(8)):
                for k in range(8):  # 回溯标记，由于棋子不动，所以8个状态位都是满的
                    visit[i][j][k] = 1
                res += dfs(idx + 1, stacks+[idx, i+1, j+1])  # 继续搜索
                for k in range(8):  # 取消标记
                    visit[i][j][k] = 0
            if pieces[idx] == "rook":  # 根据棋子选择棋子的方向
                it = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            elif pieces[idx] == "bishop":
                it = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
            else:
                it = [[1, 0], [0, 1], [-1, 0], [0, -1],
                      [1, 1], [1, -1], [-1, 1], [-1, -1]]
            for dx, dy in it:  # 遍历所有的方向
                x, y, c = i, j, 0  # 分别是起始位置和时间状态
                tmp = []  # 用于记录行进路径
                # 需要满足移动的新位置的时间状态下不存在棋子
                while 0 <= x + dx < 8 and 0 <= y + dy < 8 and visit[x + dx][y + dy][c] == 0:
                    x += dx
                    y += dy
                    c += 1
                    visit[x][y][c - 1] = 1  # 移动后需要标记当前时间状态
                    # 移动状态会维持到落子之后，需要在此方向遍历结束后才能取消标记，所以在这里先记录
                    tmp.append([x, y, c - 1])
                    if all(visit[x][y][k] == 0 for k in range(c, 8)):  # 如果之后的时间状态也不存在棋子，所以可以落子
                        for k in range(c, 8):  # 标记后续状态
                            visit[x][y][k] = 1
                        res += dfs(idx + 1, stacks+[idx, x+1, y+1])  # 继续搜索
                        for k in range(c, 8):  # 取消标记
                            visit[x][y][k] = 0
                for x, y, k in tmp:  # 将行进路径上的所有状态取消标记
                    visit[x][y][k] = 0
            return res
        l = len(pieces)
        positions = [[i - 1, j - 1] for i, j in positions]  # 坐标-1，方便计算
        visit = [[[0 for i in range(8)] for j in range(8)]
                 for k in range(8)]  # visit标记
        return dfs(0, [])

    def test(self, **kg):
        return self.countCombinations(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 102400:
            return
        if tp:
            self.draw(s[0], tp)
        self.logs += " ".join([str(v) for v in s])+"\n"

    def draw(self, s, tp: str):
        from common.tool.draw import Draw
        d = Draw()
        if tp.startswith('bar'):
            d.draw_bar_chart(s)
        elif tp.startswith('graph'):
            d.draw_graph(s)
        d.save(f"data/log/{tp}.png")

    def run(self):
        if not self.local_debug:
            return
        for case in self.get_cases():
            self.logs = ""
            self.ep = case.pop("result")
            try:
                r = self.local_debug(**case)
                self.log("finish")
            except Exception as e:
                import traceback
                traceback.print_exc()
                r = None
            if not self.diff(r, self.ep):
                print(case, 'result', r, 'except', self.ep)
                print(self.logs)
                break

    def diff(self, a, b):
        if isinstance(a, float) and isinstance(b, float):
            return "%.2f" % (a) == "%.2f" % (b)
        return a == b


if __name__ == '__main__':
    Solution().run()
