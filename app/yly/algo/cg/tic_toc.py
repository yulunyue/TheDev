

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
MAX_DEPATH = 4
from common.algo.absearch import AlphaBateSearch,AbNode,inf
from app.yly.algo.manage import SolutionBase
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


init()


class Grid3:
    def __init__(self) -> None:
        self.line_state = [0]*len(LINES)
        self.state_ct = dict()
        self.state_ct[0] = len(LINES)
        for k in SCORE_STATE:
            self.state_ct[k] = self.state_ct[-k] = 0
        self.win_state = 0
        self.grid_state = 0


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




class Grid9(Grid3):
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

class Mv(AbNode):
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
        self.state = Grid9()
        self.ab_search = AlphaBateSearch()

    def get_cases(self):
        return [
            dict(opponent_row=[],opponent_col=[],row=[],col=[],result=""),
            # dict(result="0 1", pre=[]),
        ]

    def init(self,opponent_row,opponent_col,row,col,**kw):
        pass

    def execute(self):
        mv = self.ab_search.search(self.state,4)
        return f'{mv[0]} {mv[1]}'


    def exec(self):
        while True:
            opponent_row, opponent_col = [int(i) for i in input().split()]
            valid_action_count = int(input())
            for i in range(valid_action_count):
                row, col = [int(j) for j in input().split()]
            self.init(opponent_row,opponent_col,row,col)
            print(self.execute())

if __name__ == '__main__':
    Solution().run()
