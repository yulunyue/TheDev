

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
inf = 100000000
inm = inf+1
MAX_DEPATH = 4
try:
    from app.yly.manage import SolutionBase
    from pyinstrument import Profiler
    DEV = True
except:
    DEV = False

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
POS_STATE = []
MAX_TIME = 0.2
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
        POS_STATE.append(3 << (i*2))
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
    return [y1*3+x1, y2*3+x2]


def pos2(idxpos):
    if isinstance(idxpos, Mv):
        idx, pos = idxpos.idx, idxpos.pos
    else:
        idx, pos = idxpos
    y1, x1 = idx//3, idx % 3
    y2, x2 = pos//3, pos % 3
    return [y1*3+y2, x1*3+x2]


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

    def put(self, pos, val, last_mv=None):
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

    # def calc_score(self):
    #     ans = 0
    #     for k, v in enumerate(self.state_ct):
    #         ans += STATE_SCORE.get(k, 0)*v
    #     return ans

    def get_moves(self, op):
        ret = []
        for p in POS:
            if self.grid_state & POS_STATE[p] == 0:
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
        self.play_id = 1

    def load(self):
        self.nodes: List[Grid] = []
        self.nodes_sort: List[Grid] = []
        for i in range(len(POS)):
            g = Grid()
            g.init(i)
            self.nodes.append(g)
        for n in POS:
            self.nodes_sort.append(self.nodes[n])

    def put(self, pi, op, last_mv=None, is_best=False):
        c: Grid = self.nodes[pi[0]]
        if last_mv and pos2(last_mv) == [5, 2] and pos2(pi) == [8, 6]:
            pass
        self.score += c.put(pi[1], op)
        self.score += 100*super().put(pi[0], c.win_state)
        self.play_id = 3-self.play_id

    def get_score(self, depth):
        if self.win_state == 1:
            return inm if self.play_id == 1 else -inm
        if self.win_state == 2:
            return inm if self.play_id == 2 else -inm
        return self.score if self.play_id == 1 else -self.score

    def get_moves(self, depth, last_move):
        if last_move is not None and self.nodes[last_move[1]].win_state == 0 and self.nodes[last_move[1]].grid_state.bit_count() != 9:
            ret = self.nodes[last_move[1]].get_moves(self.play_id)
        else:
            ret = []
            for n in self.nodes_sort:
                if n.win_state:
                    continue
                ret.extend(n.get_moves(self.play_id))
        # ret = sorted(ret, key=lambda v: v[2],
        #              reverse=True if op == 1 else False)[:7]
        return ret

    def get_depth(self):
        return MAX_DEPATH


class AlphaBate:
    '''
                               0,3

          1,2                  2,6               3,3

    4,8   5,2   6,7       7,1  8,?  9,?     10,3  11,6   12,9


    '''
    last_move = None

    def __init__(self) -> None:
        self.grid = Gd()

    def do(self, pos):
        self.last_move = pos
        self.grid.put(pos, self.grid.play_id)

    def absearch(self, depth, last_move=None, alpha=-inf, bate=inf) -> None:
        if depth == 0:
            return None, self.grid.get_score(depth)
        movs = self.grid.get_moves(depth, last_move)
        if not movs:
            return None, self.grid.get_score(depth)
        best_mv = movs[0]
        for mv in movs:
            self.grid.put(mv, self.grid.play_id, last_move, False)
            _, val = self.absearch(depth=depth-1, last_move=mv,
                                   alpha=-bate, bate=-alpha)
            val = -val
            if val >= bate:
                alpha = bate
                best_mv = mv
                self.grid.put(mv, 0, last_move, True)
                break
            if val > alpha:
                alpha = val
                best_mv = mv
                self.grid.put(mv, 0, last_move, True)
            else:
                self.grid.put(mv, 0, last_move, False)
        return best_mv, alpha

    def run(self):
        start_time = time.time()
        best_move, best_score = None, -inf
        for i in range(self.grid.get_depth()):
            if time.time()-start_time >= MAX_TIME:
                break
            best_move, best_score = self.absearch(
                i+1, last_move=self.last_move)
        return best_move, best_score

    def search(self):
        depth = self.grid.get_depth()
        return self.absearch(depth, last_move=self.last_move)
        # return self.run()

    @staticmethod
    def get_info(frames):
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
            try:
                pos.append([int(stdout[0]), int(stdout[2])])
            except:
                pos.append(stdout)
        return dict(
            pos=str(pos),
            nums=[min_num, max_num],
            score=[min_score, max_score]
        )

    def dump(self, *args):
        return dict(vt_num=0, score=0)


class Mv:
    def __init__(self, idx, pos, depth=None, player_id=None, parent=None) -> None:
        self.idx = idx
        self.pos = pos
        self.depth = depth
        self.player_id = player_id
        self.score = 0
        # self.pre: Mv = parent
        self.after: Mv = None

    def __str__(self) -> str:
        p = self
        ret = []
        while p:
            ret.append(str(pos2(p)))
            p = p.after
        return ",".join(ret)


class GdDev(Gd):
    def put(self, pi, op, last_mv: Mv = None, is_best=False):
        if is_best and isinstance(last_mv, Mv):
            last_mv.after = pi
        if isinstance(pi, Mv):
            pi = [pi.idx, pi.pos]
        ret = super().put(pi, op, last_mv)
        # Solution.log(pi, op)
        return ret

    def get_moves(self, depth, last_move):
        if isinstance(last_move, Mv):
            last_move = [last_move.idx, last_move.pos]
        self.vt_ct[depth] += 1
        return [Mv(*d, depth=depth, player_id=self.play_id) for d in super().get_moves(depth, last_move)]

    def get_score(self, depth):
        ret = super().get_score(None)
        self.vt_ct[depth] += 1
        return ret

    def dumps(self):
        info = [["0"]*9 for _ in range(9)]
        for pos in range(81):
            y1, x1 = pos//9, pos % 9
            pos, idx = pos1(y1, x1)
            c: Grid = self.nodes[pos]
            s = (c.grid_state >> (idx*2)) & 3
            if c.win_state and idx == 4:
                # info[y1][x1] = str(c.win_state*3+s)
                info[y1][x1] = ['0', 'X', 'O'][c.win_state]
            else:
                info[y1][x1] = str(s)
        infs = []
        for i, inv in enumerate(info):
            if i % 3 == 0:
                infs.append('\n')
            tmp = [] if i != 0 else ['   012 345 678\n']
            for j in range(3):
                tmp.append((f"{i}: " if j == 0 else "") +
                           inv[j*3]+inv[j*3+1]+inv[j*3+2]+" ")
            infs.append("".join(tmp)+"\n")

        return dict(
            infos="".join(infs),
            # score=self.calc_score()
        )

    def get_depth(self):
        ret = MAX_DEPATH
        self.vt_ct = [0]*(ret+1)
        return ret


class AlphaBateDev(AlphaBate):
    def __init__(self) -> None:
        self.grid = GdDev()

    def dump(self, mv, last_mv, score):
        infos = self.grid.dumps()
        return ";".join([
            f'---play_id:{self.grid.play_id}',
            f'mv:{mv}',
            f'lastmv:{last_mv}',
            f'score:{score}---{infos["infos"]}---vt_ct:{self.grid.vt_ct}---\n'
        ])

    def profile(self):
        self.log = lambda *args: print(*args)
        p = Profiler()
        p.start()
        p.stop()
        p.print()

    def search(self):
        return super().search()
        # return None, None


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/tic-tac-toe"
    gameid = '6246186678d52f83e9a2d47885d4b6f60900eed7'
    game_type = 'pk'
    name = "tic_toc"
    agentsIds = [
        # 5604295,
        -2, -1
    ]

    def __init__(self) -> None:
        self.ai = AlphaBate() if not DEV else AlphaBateDev()

    def get_cases(self):
        return [
            # dict(result="", pre=[[0, 0]]),
            # dict(result="", pre=[[-1, -1]]),
            dict(result="", pre=0),
            # dict(result="0 1", pre=[]),
        ]

    def get_cases(self):
        data = json.load(
            open("data/log/codingame/tic_toc.main.json", 'r'))
        pres = json.loads(data["pos"])
        return [
            dict(pre=pres[:i], result="")
            for i in range(1, len(pres), 2)
        ]

    @ staticmethod
    def get_info(frames, *args, **kwargs):
        return AlphaBate.get_info(frames)

    def execute(self, pre, **kg):
        for row, col in pre:
            if row >= 0 and col >= 0:
                self.ai.do(pos1(row, col))
        mv, score = self.ai.search()
        self.log(self.ai.dump(mv, pre[-2:], score))
        if mv:
            self.ai.do(mv)
            mv = pos2(mv)
            return f'{mv[0]} {mv[1]}'
        return f'9 9'


if __name__ == '__main__':
    Solution().run()
