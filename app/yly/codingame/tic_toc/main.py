

import time
from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import bisect
import sys
import math
import heapq
import json
import json
inf = float("inf")

try:
    from app.yly.manage import SolutionBase
    from pyinstrument import Profiler
    DEV=True
except:
    DEV=False
    class SolutionBase:
        def input(self):
            return input()

        def log(self, info):
            print(json.dumps(info), file=sys.stderr, flush=True)

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
LINES = [
    [0, 1, 2, 0],
    [3, 4, 5, 0],
    [6, 7, 8, 0],
    [0, 3, 6, 0],
    [1, 4, 7, 0],
    [2, 5, 8, 0],
    [0, 4, 8, 0],
    [2, 4, 6, 0]
]
POS = [4, 1, 3, 5, 7, 0, 2, 6, 8]
G = [[] for _ in range(9)]
STATE_MASK = []
WIN1 = [[1, 1, 1]]
KONG1 = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
KONG2 = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
# WIN1 = 9+3+1
# KONG1 = [9+1, 9+3, 1+3]
# KONG2 = [1, 3, 9]
SCORE0, SCORE1, SCORE2, SCORE3 = 0, 1, 10, 100
SCORE_STATE = {
    SCORE3: WIN1,
    SCORE2: KONG1,
    SCORE1: KONG2
}
MASK_GRID = (2 << 17)-1
STATE_SCORE = [0]*MASK_GRID
MASK_POS = (1 << 9)-1


def init():
    for i in range(9):
        STATE_MASK.append(MASK_GRID ^ (3 << (i*2)))
    for i, v2 in enumerate(LINES):

        for v1 in v2[:3]:
            v2[3] |= 3 << (v1*2)
            G[v1].append(i)

    for score, states in SCORE_STATE.items():
        for i, line in enumerate(LINES):
            for a1, a2, a3 in states:
                s2 = (a1 << line[0]*2)+(a2 << line[1]*2)+(a3 << line[2]*2)
                # print(bin(s2), bin(s2*2))
                STATE_SCORE[s2] = score
                STATE_SCORE[s2*2] = -score


def pos1(i, j):
    y1, y2 = i//3, i % 3
    x1, x2 = j//3, j % 3
    return y1*3+x1, y2*3+x2


def pos2(idx, pos, *args):
    y1, x1 = idx//3, idx % 3
    y2, x2 = pos//3, pos % 3
    return y1*3+y2, x1*3+x2


# def s(v, i, j):
#     return (v >> (LINES[i][j]*2) & 3) << j*2


def setbit(x, n):
    return x | 1 << n


def clrbit(x, n):
    return x & ~(1 << n)


init()


class Grid:
    def __init__(self) -> None:
        self.line_state = [0]*len(LINES)
        self.state_ct = dict()
        self.state_ct[0] = len(LINES)
        for k in SCORE_STATE:
            self.state_ct[k] = self.state_ct[-k] = 0

        self.win_state = 0
        # self.pos_state = MASK_POS
        self.grid_state = 0
        # self.states = [0]*9

    def init(self, idx):
        self.idx = idx

    def put(self, pos, val):
        self.grid_state = (
            self.grid_state & STATE_MASK[pos]) | (val << (pos*2))
        # self.states[pos] = val
        return self.update(pos)

    def update(self, pos):
        # lct = len(G[pos])
        ans = 0
        for i in G[pos]:
            new_state = self.grid_state & LINES[i][3]
            # new_state = self.states[LINES[i][0]]*9 + \
            #     self.states[LINES[i][1]]*3+self.states[LINES[i][2]]
            # if new_state not in STATE_SCORE:
            #     lct -= 1
            ans += STATE_SCORE[new_state] - STATE_SCORE[self.line_state[i]]
            self.state_ct[STATE_SCORE[self.line_state[i]]] -= 1
            self.line_state[i] = new_state
            self.state_ct[STATE_SCORE[new_state]] += 1
        # self.pos_state = setbit(
        #     self.pos_state, pos) if lct else clrbit(self.pos_state, pos)
        if self.state_ct[SCORE3]:
            self.win_state = 1
        elif self.state_ct[-SCORE3]:
            self.win_state = 2
        # elif self.pos_state == 0:
        #     self.win_state = 3
        else:
            self.win_state = 0
        return ans

    def calc_score(self):
        ans = 0
        for k, v in enumerate(self.state_ct):
            ans += STATE_SCORE.get(k, 0)*v
        return ans

    def get_moves(self, op):
        ret = []
        for p in POS:
            if self.grid_state >> (p*2) & 3 == 0:
                ret.append([self.idx, p])
        return ret

    def to_json(self):
        return dict(

        )


class Gd(Grid):
    def __init__(self):
        super().__init__()
        self.load()
        self.score = 0

    def load(self):
        self.nodes: List[Grid] = []
        for i in range(9):
            g = Grid()
            g.init(i)
            self.nodes.append(g)

    def put(self, pos, idx, op):
        c: Grid = self.nodes[pos]
        self.score += c.put(idx, op)
        self.score += 100*super().put(pos, c.win_state)

    def calc_score(self):
        return 100*super().calc_score()+sum(c.calc_score() for c in self.nodes)

    def get_score(self, val):
        return self.score if val == 1 else -self.score

    def get_moves(self, pos, op):
        if pos is not None and self.nodes[pos].win_state == 0:
            ret = self.nodes[pos].get_moves(op)
        else:
            ret = []
            for n in self.nodes:
                if n.win_state:
                    continue
                ret.extend(n.get_moves(op))
        # ret = sorted(ret, key=lambda v: v[2],
        #              reverse=True if op == 1 else False)[:7]
        return ret

    def dumps(self):
        info = [["0"]*9 for _ in range(9)]
        for pos in range(81):
            y1, x1 = pos//9, pos % 9
            pos, idx = pos1(y1, x1)
            c: Grid = self.nodes[pos]
            s = (c.grid_state >> (idx*2)) & 3
            if c.win_state:
                info[y1][x1] = str(c.win_state+3)
            else:
                info[y1][x1] = str(s)
        infs = []
        for i, inv in enumerate(info):
            if i % 3 == 0:
                infs.append('\n')
            tmp = []
            for j in range(3):
                tmp.append(inv[j*3]+inv[j*3+1]+inv[j*3+2]+" ")
            infs.append("".join(tmp)+"\n")

        return dict(
            infos="".join(infs),
            score=self.calc_score()
        )


class AlphaBate:
    '''
                               0,3

          1,2                  2,6               3,3

    4,8   5,2   6,7       7,1  8,?  9,?     10,3  11,6   12,9


    '''

    def __init__(self, max_depth, max_time) -> None:
        self.max_depth = max_depth
        self.max_time = max_time
        self.grid = Gd()
        self.max_time = max_time
        self.grid = Gd()
        self.play_id=1

    def evaluate(self,depth):
        return self.grid.get_score(self.play_id)

    def put(self, *args):
        self.grid.put(*args)

    def end_search(self, depth):
        return depth >= self.max_depth

    def do(self, pos, idx):
        self.put(pos, idx, self.play_id)
        self.play_id=3-self.play_id

    def undo(self, pos, idx):
        self.put(pos, idx, 0)
        self.play_id=3-self.play_id

    def get_moves(self,last_mv):
        if not last_mv:
            return self.grid.get_moves(None)
        return self.grid.get_moves(last_mv)

    def search(self, depth, last_mv=None,alpha=-inf, bate=inf) -> None:
        if depth == 0:
            return None, self.evaluate(depth)
        movs = self.get_moves(last_mv)
        if not movs:
            return None, self.evaluate(depth)
        best_mv = None
        for mv in movs:
            self.do(*mv)
            _, val = self.search(depth=depth-1,last_mv=mv,alpha=-bate, bate=-alpha)
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
        start_time = time.time()
        best_move, best_score = None, -inf
        for i in range(self.max_depth):
            if time.time()-start_time >= self.max_time:
                break
            best_move, best_score = self.search(i+1)
        return best_move, best_score

    def get_depth(self):
        return 4+(len(self.pos)//100)

    def search2(self):
        depth=self.get_depth()
        return self.search(depth)

class AlphaBateDebug(AlphaBate):
    pass

class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/tic-tac-toe"
    gameid = '6246186678d52f83e9a2d47885d4b6f60900eed7'
    game_type = 'pk'
    agentsIds = [
        # 5604295,
        -2, -1
    ]

    def __init__(self) -> None:
        self.ai = AlphaBate() if not DEV else AlphaBateDebug()

    def get_cases(self):
        return [
            # dict(result="0 1",pre=[[-1,-1]]),
            dict(result="0 1", pre=[[4, 4], [3, 3], [0, 0]]),
        ]

    def draw(self, mv, score):
        # [pos2(*v) for v in self.ai.pos]

        info = self.ai.grid.dumps()
        self.log(
            f"----mv:{mv},pos:{len(self.ai.pos)},score_calc:{info['score']},score_add:{self.ai.grid.score}")
        self.log(info['infos'])
        self.log(f"----score:{score}")

    @staticmethod
    def get_info(frames, *args, **kwargs):
        pos = []
        min_num, max_num, min_score, max_score = inf, -inf, inf, -inf
        for frame in frames:
            stdout = frame.get("stdout")
            if not stdout:
                continue
            if 'stderr' in frame:
                jl = json.loads(frame['stderr'])
                min_num, max_num = min(jl['vt_num'], min_num), max(
                    jl['vt_num'], max_num)
                min_score, max_score = min(
                    jl['score'], min_score), max(jl['score'], max_score)
            pos.append([int(stdout[0]), int(stdout[2])])
        return dict(
            pos=str(pos),
            nums=[min_num, max_num],
            score=[min_score, max_score]
        )

    def execute(self, pre, **kg):
        for row, col in pre:
            if row >= 0 and col >= 0:
                self.ai.do(*pos1(row, col))
        mv, score = self.ai.search2()
        # if len(pre) > 1:
        #     self.draw(mv, score)
        self.log(dict(vt_num=self.ai.vt_num, score=score))
        if mv:
            self.ai.do(*mv)
            mv = pos2(*mv)
            return f'{mv[0]} {mv[1]}'
        return f'-1 -1'

    def profile(self):
        self.log = lambda *args: print(*args)
        p = Profiler()
        p.start()
        self.execute([[4, 4], [3, 3], [2, 2], [6, 8], [2, 8], [6, 7], [2, 4], [7, 3], [5, 1], [7, 5], [5, 6], [8, 1], [8, 3], [8, 0], [7, 2], [3, 7], [1, 5], [3, 6], [1, 2], [3, 8], [1, 7], [
                     4, 3], [4, 0], [4, 1], [5, 4], [8, 5], [8, 7], [6, 4], [1, 3], [5, 0], [7, 0], [3, 2], [2, 7], [8, 4], [6, 5], [2, 6], [6, 2], [0, 7], [0, 4], [2, 3], [8, 2], [8, 8], [8, 6]])
        p.stop()
        p.print()



if __name__ == '__main__':
    Solution().run()
