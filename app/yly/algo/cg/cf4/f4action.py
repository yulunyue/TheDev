from app.yly.algo.cg.cf4.f4state import F4State, StateEnum, Action, S, C


class KaggleEnv:

    def __init__(self, board, rows, columns, mark):
        self.board = board
        self.rows = rows
        self.columns = columns
        self.mark = mark
        self.inarow = 4


class F4Action(Action):
    dst: F4State
    src: F4State = None
    action = None

    def load(self, src, y, x, dst, reward=0):
        self.y, self.x = y, x
        return super().load(src, x, dst, reward)

    def get_action_str(self):
        return f"[y={self.y}][x={self.x}][p={S[1-self.dst.player_id]}]"

    def get_reward(self, params: StateEnum, **kwargs):
        score = 0
        for k, v1 in self.dst.state.items():
            v2 = 0 if self.src is None else self.src.state[k]
            score += params._params[k].get_value() * (v1 - v2)
        return score

    def load_from_kaggle(self, obs: KaggleEnv, conf: KaggleEnv):
        self.dst = F4State(obs.board).init_root(conf.rows, conf.columns)
        return self

    def laod_from_karord(self, board, action):
        self.board = board
        self.action = action
        return self

    def dump_to_kaggle(self):
        c = KaggleEnv(self.dst.grid, C.HEIGHT, C.WIDTH, self.dst.player_id + 1)
        return c, c

    def load_from_state(self, state=None, height=7, width=9):
        self.dst = F4State(state).init_root(height, width)
        return self

    def set_info_from_kg1(self, grid=None):
        if grid:
            info = grid[self.x][C.HEIGHT - 1 - self.y]
            for k in ["swarm_patterns", "opp_patterns"]:
                for k1, v in info[k].items():
                    info[k][k1] = "".join([("?" + S)[v1["mark"]] for v1 in v])
            info["point_len"] = dict()
            for y in range(C.HEIGHT - self.y):
                info["point_len"][y] = len(grid[self.x][y]["points"])
            self.grid = info["points"]
        else:
            info = dict()
            for k, v1 in self.dst.state.items():
                src = 0 if self.src is None else self.src.state[k]
                info[k] = v1 - src

        self.set_info(info)
