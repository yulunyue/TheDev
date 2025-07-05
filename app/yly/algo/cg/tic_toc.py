from collections import defaultdict
from common.algo.search.state import AlphaBateSearch, AbNode, inf
from common.algo.manage import SolutionBase, View
from typing import List, Dict

POS = [4, 1, 3, 5, 7, 0, 2, 6, 8]
POS_LINE = [[] for _ in range(len(POS))]
LINES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]
PLAYER_OP = 1
PLAYER_SELF = 2
PLAYER_NULL = 0
SCORE_MAP = dict()


def get_score(a, b, c, v):
    s1 = a * 9 + b * 3 + c
    SCORE_MAP[s1] = v

    def u(g):
        return 2 if g == 1 else 0

    d, e, f = u(a), u(b), u(c)
    s2 = d * 9 + e * 3 + f
    SCORE_MAP[s2] = -v
    return [s1, s2]


WIN = get_score(1, 1, 1, 100)


def init():
    for i, l in enumerate(LINES):
        for j, v in enumerate(l):
            POS_LINE[v].append([i, j])


init()


class Grid3:
    def __init__(self):
        self.grid = [0] * 9
        self.lines = [[0] * 3 for _ in LINES]
        self.line_state = [0] * len(LINES)
        self.state_ct = defaultdict(int)
        self.score = 0

    def put3(self, pos, val):
        self.grid[pos] = val
        score = 0
        for i, j in POS_LINE[pos]:
            self.lines[i][j] = val
            state = self.lines[i][0] * 9 + self.lines[i][1] * 3 + self.lines[i][1]
            score += self.set_state(i, state)
        if self.state_ct[WIN[0]]:
            return 1, score
        if self.state_ct[WIN[1]]:
            return 2, score
        return 0, score

    def set_state(self, i, state):
        self.state_ct[self.line_state[i]] -= 1
        self.state_ct[state] += 1
        ret = SCORE_MAP.get(state, 0) - SCORE_MAP.get(self.line_state[i], 0)
        self.line_state[i] = state
        return ret

    # def get_moves(self):
    #     return [p for p in POS if self.grid[p]==0]


class Grid9(Grid3):
    def __init__(self):
        super().__init__()
        self.grid3: List[Grid3] = [Grid3() for _ in range(9)]

    def put(self, i: int, j: int, op):
        self.i, self.j = i, j
        op1, score1 = self.grid3[self.i].put3(self.j, op)
        op2, score2 = self.put3(self.i, op1)
        self.score += score2 * 100 + score1


G = Grid9()


class Move(AbNode):
    MAX_DEPATH = 1

    def __init__(self, y, x, op) -> None:
        self.y = y
        self.x = x
        self.op = op
        self.key = f"{y},{x},{op}"
        super().__init__()

    def do(self):
        G.put(self.y, self.x, self.op)
        return self

    def get_nexts(self, depth):
        if depth >= Move.MAX_DEPATH:
            return []
        return [
            Move(self.x, i, 3 - self.op).set_depth(depth + 1)
            for i, v in enumerate(G.grid3[self.x].grid)
            if v == PLAYER_NULL
        ]

    def calc_value(self, depth):
        return G.score if depth % 2 else -G.score


class AbS(AlphaBateSearch):
    pass


class Solution(SolutionBase):

    game_type = "pk"
    name = "tic_toc"

    _has_view = True

    def __init__(self) -> None:
        self.search = AbS()
        self.op = PLAYER_OP
        self.mv: Move = None
        self.moves: List[Move] = []

    def do(self, y, x):
        self.mv = Move(y, x, self.op).do()
        self.moves.append(self.mv)
        self.op = 3 - self.op

    def get_watch(self):
        return [
            # View("mvs").grid()
            View("mv").graph()
        ]

    def get_cases(self):
        return [
            dict(mvs=[[4, 4]], result=""),
            # dict(mvs=[],result=""),
        ]

    def init_env(self, opponent_row, opponent_col, row, col, **kw):
        if opponent_row != -1 and opponent_col == -1:
            self.mv = self.do(opponent_row, opponent_col)

    def init(self, mvs, search_depth=2, **kw):
        self.moves.clear()
        Move.MAX_DEPATH = search_depth
        for y, x in mvs:
            self.do(y, x)

    def execute(self):
        if self.mv:
            self.search.search(self.mv)
            self.mv = self.mv.best_action
        else:
            self.mv = Move(4, 4, self.op)
        self.do(self.mv.y, self.mv.x)
        y1, x1, y2, x2 = self.mv.y // 3, self.mv.y % 3, self.mv.x // 3, self.mv.x % 3
        return f"{y1*3+y2} {x1*3+x2}"

    def exec(self):
        while True:
            opponent_row, opponent_col = [int(i) for i in input().split()]
            valid_action_count = int(input())
            for i in range(valid_action_count):
                row, col = [int(j) for j in input().split()]
            self.init_env(opponent_row, opponent_col, row, col)
            self.output(self.execute())


if __name__ == "__main__":
    Solution().run()
