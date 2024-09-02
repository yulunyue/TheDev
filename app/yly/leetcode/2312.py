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
            dict(grid=[[0, 0, 0, 0, 0], [0, 2, 0, 2, 0], [0, 2, 0, 2, 0], [
                 0, 2, 1, 2, 0], [0, 2, 2, 2, 0], [0, 0, 0, 0, 0]], result=1),
            dict(grid=[[0, 2, 0, 0, 1], [0, 2, 0, 2, 2], [0, 2, 0, 0, 0], [
                 0, 0, 2, 2, 0], [0, 0, 0, 0, 0]], result=0),
            dict(grid=[[0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 1, 0], [
                 0, 2, 0, 0, 1, 2, 0], [0, 0, 2, 2, 2, 0, 2], [0, 0, 0, 0, 0, 0, 0]], result=3)
        ]

    def maximumMinutes(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        dr = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        def get_next(y, x):
            ret = []
            for ay, ax in dr:
                ny, nx = y+ay, x+ax
                if ny < 0 or nx < 0 or ny >= n or nx >= m:
                    continue
                if grid[ny][nx] == 2:
                    continue
                ret.append([ny, nx])
            return ret

        fire_grass_time = [[inf for _ in range(m)] for _ in range(n)]
        fire = []
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 1:
                    fire.append([0, i, j])
                    fire_grass_time[i][j] = 0
        while fire:
            e_fire = fire
            fire = []
            for t, i, j in e_fire:
                for y, x in get_next(i, j):
                    if fire_grass_time[y][x] == inf:
                        fire_grass_time[y][x] = t+1
                        fire.append((t+1, y, x))
        # self.log(grid,tp="grid")
        self.log(fire_grass_time, tp='grid')
        p = dict()

        def get_min(cur, step):
            ret = fire_grass_time[cur[0]][cur[1]]-step
            self.log('head', cur, fire_grass_time[cur[0]][cur[1]], step, ret)
            while cur in p:
                cur = p[cur]
                ret = min(ret, fire_grass_time[cur[0]][cur[1]]-step)
                self.log("get_p", cur, step,
                         fire_grass_time[cur[0]][cur[1]], ret)
                step -= 1

            return 10**9 if ret == inf else ret
        vt = [[-1 for _ in range(m)] for _ in range(n)]

        def dfs(i, j, step, ret):
            vt[i][j] = step
            if i == n-1 and j == m-1:
                return ret
            for y, x in get_next(i, j):
                if vt[y][x] != -1:
                    continue
                max_step = fire_grass_time[y][x]
                if max_step <= step+1:
                    continue
                ret = min(dfs(y, x, step+1, ret), max_step-step-1)
            return ret
        ans = dfs(0, 0, 0, inf)
        self.log("xx")
        self.log(vt, tp='grid')
        return ans

    def test(self, **kg):
        return self.xx(**kg)

    def __init__(self, *args) -> None:
        self.local_debug = getattr(self, sys.argv[-1], None)
        if self.local_debug is None:
            print(sys.argv[-1], "not find")
    logs = ""

    def log(self, *s, tp: str = ""):
        if not self.local_debug or len(self.logs) >= 102400:
            return
        if tp:
            s2 = self.draw(s[0], tp)
            if s2:
                self.logs += str(s2)+"\n"
        else:
            self.logs += " ".join([str(v) for v in s])+"\n"

    def draw(self, s, tp: str):
        if tp == 'grid':
            return "\n".join([str(v) for v in s])
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
