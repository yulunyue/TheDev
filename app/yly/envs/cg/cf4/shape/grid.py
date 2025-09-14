from .line import Line
from .colunm import Point, Column
from common.algo.base.bin_util import low_bits, set_mask
from common.util.export import List, logger, defaultdict
from ..model.constant import C


class Grid:
    GIRD_MAP = dict()

    def load(self, shape):
        self.shape = shape
        self.height, self.width = C.SHAPES[shape]
        self.columns: List[Column] = []
        self.board = -1
        self.line_cf = [[{}, {}, {}, {}, {}], [{}, {}, {}, {}, {}]]
        for i in range(self.width):
            self.columns.append(Column(self, i, self.height))
        self.load_lines()
        return self

    def load_lines(self):
        for i in range(self.width):
            for j in range(self.height):
                for k, (dy, dx) in enumerate(C.DR):
                    y, x = i + dy * 3, j + dx * 3
                    if y < 0 or x < 0 or y >= self.height or x >= self.width:
                        continue
                    ln = Line.new_line(y, x, k)
                    for m in range(4):
                        y1, x1 = i + m * dy, j + m * dx
                        ln.set_point(m, self.columns[x1].pts[y1])

    @staticmethod
    def new(shape: int) -> "Grid":
        if shape not in Grid.GIRD_MAP:
            Grid.GIRD_MAP[shape] = Grid().load(shape)
        return Grid.GIRD_MAP[shape]

    def line_state_change(self, ln: Line, pos_idx, player_id, f0, t0, f1, t1):
        s0, s1 = f0 + t0, f1 + t1
        if (f0 == 0 or t0 == 0) and s0 >= 2:
            p0 = 0 if f0 else 1
            self.line_cf[p0][s0].pop(ln.k)

        if (f1 == 0 or t1 == 0) and s1 >= 2:
            if f1:
                p1 = 0
                if f1 == 4:
                    self.done = 0
            if t1:
                p1 = 1
                if t1 == 4:
                    self.done = 1
            self.line_cf[p1][s1][ln.k] = ln

    def set_board(self, board, player_id):

        if self.board == board:
            return self.done, self.action
        # logger.map(src_board=self.board, dst_borad=board)
        self.board = board
        self.done = None
        self.pos_score = [0, 0]
        for c in self.columns:
            c.set_state(board & c.mask)
            self.pos_score[0] += c.player_pos_score[0]
            self.pos_score[1] += c.player_pos_score[1]
            board = board >> self.height
        self.action = self.get_actions(player_id)
        if not self.action and self.done is None:
            self.done = 2
        return self.done, self.action

    def get_actions(self, player_id):
        ret = dict()
        for idx, c in enumerate(self.columns):
            if c.top == self.height - 1:
                continue
            ret[idx] = C.mask_encode(
                self.board,
                self.shape,
                idx * self.height + c.top,
                player_id,
            )

        return ret
