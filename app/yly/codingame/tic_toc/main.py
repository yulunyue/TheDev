

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
inf = float("inf")


try:
    from app.yly.manage import SolutionBase
except:
    class SolutionBase:
        def input(self):
            return input()

        def log(self, *args, **kwargs):
            pass

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            while True:
                opponent_row, opponent_col = [int(i) for i in input().split()]
                valid_action_count = int(input())
                for i in range(valid_action_count):
                    row, col = [int(j) for j in input().split()]

                # Write an action using print
                # To debug: print("Debug messages...", file=sys.stderr, flush=True)
                print(self.execute(pre=[[opponent_row, opponent_col]]))
LINES = [[] for _ in range(3)]
G = [[[] for _ in range(3)] for _ in range(3)]


def init():
    for i in range(3):
        row = []
        for j in range(3):
            row.append([i, j])
            LINES[j].append([j, i])
        LINES.append(row)
    LINES.extend([
        [[0, 0], [1, 1], [2, 2]],
        [[0, 2], [1, 1], [2, 0]]
    ])
    for i, v in enumerate(LINES):
        G[v[0]][v[1]].append(i)


init()


class Grid:
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
        self.gird = [[0]*3 for _ in range(3)]
        self.line_state = [0]*len(LINES)
        self.win = 0

    def put(self, y, x, val):
        self.gird[y][x] = val
        for i in range(len(LINES)):
            self.line_state[i] |= 3*val

    def get_moves(self):
        ret = []
        for i, row in enumerate(self.gird):
            for j, x in enumerate(row):
                if x == -1:
                    ret.append([self.i, i, self.j, j])
        return ret


def pos1(i, j):
    return i//3, i % 3, j // 3, j % 3


def pos2(i, y, j, x):
    return i*3+y, j*3+x


class AlphaBate:
    '''
                               0,3

          1,2                  2,6               3,3

    4,8   5,2   6,7       7,1  8,?  9,?     10,3  11,6   12,9   


    '''

    def __init__(self, max_depth) -> None:
        self.max_depth = max_depth
        self.grids: List[List[Grid]] = [[Grid(i, j) for j in range(3)]
                                        for i in range(3)]
        self.pos = []

    def evaluate(self):
        return 0

    def put(self, i, j, y, x, op):
        self.grids[i][j].put(y, x, op)

    def end_search(self, depth):
        return depth >= self.max_depth

    def do(self, i, y, j, x):
        self.put(i, j, y, x, 1+(len(self.pos) % 2))
        self.pos.append([i, y, j, x])

    def undo(self, i, y, j, x):
        self.put(i, j, y, x, 0)
        self.pos.pop()

    def get_moves(self):
        ret = []
        if not self.pos:
            for row in self.grids:
                for c in row:
                    ret.extend(c.get_moves())
            return ret
        i, y, j, x = self.pos[-1]
        return self.grids[y][x].get_moves()

    def search(self, depth=0, alpha=-inf, bate=inf) -> None:
        if self.end_search(depth):
            return None, self.evaluate()
        best_mv = None
        for mv in self.get_moves():
            self.do(*mv)
            _, val = self.search(depth=depth+1, alpha=-bate, bate=-alpha)
            val = -val
            self.undo(*mv)
            if val >= bate:
                alpha = bate
                best_mv = mv
                break
            if val > alpha:
                alpha = val
                best_mv = mv
        return best_mv, alpha


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/tic-tac-toe"
    gameid = '6246186678d52f83e9a2d47885d4b6f60900eed7'
    game_type = 'pk'

    def __init__(self) -> None:
        self.ai = AlphaBate(8)

    def get_cases(self):
        return [
            dict(result="0 1", pre=[[0, 1], [2, 4]])
        ]

    def draw(self):
        info = [["?"]*9 for _ in range(9)]
        for pos in range(81):
            y1, x1 = pos//9, pos % 9
            i, y, j, x = pos1(y1, x1)
            s = self.ai.grids[i][j].gird[y][x]
            info[y1][x1] = ['?', '*', '#'][s]
        self.log("----\n"+"\n".join("".join(iof) for iof in info)+"\n----\n")

    def execute(self, pre, **kg):
        for row, col in pre:
            if row >= 0 and col >= 0:
                self.ai.do(*pos1(row, col))
        mv, _ = self.ai.search()
        self.ai.do(*mv)
        mv = pos2(*mv)
        # self.draw()
        # self.log(self.ai.pos, mv, pre)
        return f'{mv[0]} {mv[1]}'


if __name__ == '__main__':
    Solution().run()
