

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
import json
inf = float("inf")
import time
import _thread

try:
    from app.yly.manage import SolutionBase
except:
    class SolutionBase:
        def input(self):
            return input()

        def log(self, *args, **kwargs):
            print(f"Debug messages...{args}", file=sys.stderr, flush=True)

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
WIN1=9+3+1
WIN2=2*(9+3+1)
SCORE_MAP={
    4:[1+3,3+9,1+9],
    100:[WIN1]
}

def init():
    for i in range(3):
        row = []
        for j in range(3):
            row.append([i, j])
            LINES[j].append([i, j])
        LINES.append(row)
    LINES.extend([
        [[0, 0], [1, 1], [2, 2]],
        [[0, 2], [1, 1], [2, 0]]
    ])
    for i, v2 in enumerate(LINES):
        for v1 in v2:
            G[v1[0]][v1[1]].append(i)

def pos1(i, j):
    return i//3, i % 3, j // 3, j % 3

def pos2(i, y, j, x):
    return i*3+y, j*3+x

init()

class Nd:
    def __init__(self):
        self.win=0

class Grid:
    def __init__(self) -> None:
        self.line_state = [0]*len(LINES)
        self.win = 0
        self.state_ct=[0]*27
        self.state_ct[0]=len(LINES)

    def init(self,i,j):
        self.i = i
        self.j = j
        self.grid = [[Nd() for _ in range(3)] for _ in range(3)]

    def put(self, y, x, val):
        self.grid[y][x].win = val
        self.update(y,x)

    def update(self,y,x):
        for i in G[y][x]:
            s1,s2,s3=[self.grid[LINES[i][j][0]][LINES[i][j][1]].win for j in range(3)]
            self.state_ct[self.line_state[i]]-=1
            self.line_state[i] = s1*9+s2*3+s3
            self.state_ct[self.line_state[i]]+=1
        if self.state_ct[WIN1]:
            self.win=1
        elif self.state_ct[WIN2]:
            self.win=2
        else:
            self.win=0
    def get_score(self,val):
        ans=0
        for k in SCORE_MAP:
            for v1 in SCORE_MAP[k]:
                ans+=(self.state_ct[v1*2]-self.state_ct[v1])*k
        return ans if val==2 else -ans
    def get_moves(self):
        ret = []
        for i, row in enumerate(self.grid):
            for j, x in enumerate(row):
                if x.win == 0:
                    ret.append([self.i, i, self.j, j])
        return ret

    def to_json(self):
        return dict(
            i=self.i,
            j=self.j,
            win=self.win,
            score=self.get_score(2),
            grid=",".join("".join(str(w1.win) for w1 in w) for w in self.grid)
        )

class Gd(Grid):
    def __init__(self):
        super().__init__()
        self.load()

    def load(self):
        self.grid = []
        self.nodes:List[Grid]=[]
        for i in range(3):
            self.grid.append([])
            for j in range(3):
                g=Grid()
                g.init(i,j)
                self.grid[-1].append(g)
                self.nodes.append(g)
            
    def put(self,i,j,y,x,op):
        c:Grid=self.grid[i][j]
        c.put(y,x,op)
        self.update(i,j)

    def get_score(self, val):
        return super().get_score(val)*100+sum(n.get_score(val) for n in self.nodes)
    def get_moves(self,y,x):
        if y is not None and self.grid[y][x].win==0:
            return self.grid[y][x].get_moves()
        ret=[]
        for n in self.nodes:
            if n.win:
                continue
            ret.extend(n.get_moves())
        return ret

class AlphaBate:
    '''
                               0,3

          1,2                  2,6               3,3

    4,8   5,2   6,7       7,1  8,?  9,?     10,3  11,6   12,9   


    '''

    def __init__(self, max_depth,max_time) -> None:
        self.max_depth = max_depth
        self.max_time = max_time
        self.grid = Gd()
        self.pos = []

    def evaluate(self):
        return self.grid.get_score(1+(len(self.pos)%2))

    def put(self, i, j, y, x, op):
        self.grid.put(i,j, y, x, op)

    def end_search(self, depth):
        return depth >= self.max_depth

    def do(self, i, y, j, x):
        self.put(i, j, y, x, 1+(len(self.pos) % 2))
        self.pos.append([i, y, j, x])

    def undo(self, i, y, j, x):
        self.put(i, j, y, x, 0)
        self.pos.pop()

    def get_moves(self):
        if not self.pos:
            return self.grid.get_moves(None,None)
        _, y, _, x = self.pos[-1]
        return self.grid.get_moves(y,x)

    def search(self, depth, alpha=-inf, bate=inf) -> None:
        if depth==0:
            return None, self.evaluate()
        best_mv = None
        for mv in self.get_moves():
            self.do(*mv)
            _, val = self.search(depth=depth-1, alpha=-bate, bate=-alpha)
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
    def run(self):
        start_time=time.time()
        best_move,best_score=None,-inf
        for i in range(self.max_depth):
            if time.time()-start_time>=self.max_time:
                break
            best_move,best_score=self.search(i+1)
        return best_move,best_score


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/tic-tac-toe"
    gameid = '6246186678d52f83e9a2d47885d4b6f60900eed7'
    game_type = 'pk'

    def __init__(self) -> None:
        self.ai = AlphaBate(6,0.09)

    def get_cases(self):
        return [
            dict(result="0 1", pre=[(0, 0), (2, 1), (6, 3), (2, 0)]),
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
        mv, score = self.ai.run()
        self.log(json.dumps(dict(
            mv=mv, score=score,
            pre=[pos2(*v) for v in self.ai.pos],
            grid=[v.to_json() for v in self.ai.grid.nodes],
        )))
        self.ai.do(*mv)
        mv = pos2(*mv)
        return f'{mv[0]} {mv[1]}'


if __name__ == '__main__':
    Solution().run()
