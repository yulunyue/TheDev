from app.yly.game.envs.cf4.shape.line import Line
from app.yly.game.envs.cf4.shape.colunm import Point, Column
from common.algo.base.bin_util import low_bits, set_mask
from common.util.export import List, logger, defaultdict
from app.yly.game.envs.cf4.model.constant import C


class Grid:
    GIRD_MAP = dict()

    def load(self, shape):
        self.shape = shape
        self.height, self.width = C.SHAPES[shape]
        self.columns: List[Column] = []
        self.board = 0
        self.line_ct = defaultdict(int)
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
                    m = 0
                    while m <= 3:
                        y, x = i + m * dy, j + m * dx
                        ln.set_point(m, self.columns[y].pts[x])
                        m += 1

    @staticmethod
    def new(shape: int) -> "Grid":
        if shape not in Grid.GIRD_MAP:
            Grid.GIRD_MAP[shape] = Grid().load(shape)
        return Grid.GIRD_MAP[shape]

    def line_state_change(self, ln: Line, pos_idx, player_id, f0, t0, f1, t1):
        self.line_ct[f0, t0] -= 1
        self.line_ct[f1, t1] += 1
        # logger.map(
        #     ln=ln, pt=ln.pts[pos_idx], player_id=player_id, ct=dict(self.line_ct)
        # )

    def set_board(self, board):

        if self.board == board:
            return self
        # logger.map(src_board=self.board, dst_borad=board)
        self.done = None
        self.board = board
        for c in self.columns:
            c.set_state(board & c.mask)
            board = board >> self.height
        if self.line_ct[4, 0]:
            self.done = 0
        elif self.line_ct[0, 4]:
            self.done = 1
        return self

    def get_actions(self, player_id):
        ret = []
        for c in self.columns:
            if c.top == self.height:
                continue
            a = dict(action=c.idx, mask=c.put(player_id))
            ret.append(a)

        return ret

    def to_str(self):
        ret = [["-"] * self.width for _ in range(self.height)]
        for i in range(self.width):
            co = self.columns[i]
            for j in range(co.top - 1, -1, -1):
                ret[self.height - j - 1][i] = str(co.pts[j].value)
        return "\n".join([" ".join(s) for s in ret] + ["-" * (2 * self.width - 1)])
