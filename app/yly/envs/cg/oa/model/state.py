from common.algo.search.state import State, Action
from common.algo.search.state import Action
from common.algo.search.algo import Algo
from common.util.export import List
from app.yly.envs.cg.oa.model.constant import C


class Rooms(State):

    STATE_MAP = dict()

    def __init__(self, state=None):
        super().__init__(state)
        self.player_id, self.curent_round, score0, score1, *self.boards = C.decode_data(
            state
        )
        self.score = [score0, score1]

    @staticmethod
    def new(state) -> "Rooms":
        if state not in Rooms.STATE_MAP:
            Rooms.STATE_MAP[state] = Rooms(state)
        return Rooms.STATE_MAP[state]

    def make_actions(self, *args, **kw):
        self.actions = dict()
        self_start = self.player_id * C.SELF_NUM
        self_end = self_start + C.SELF_NUM

        for i in range(C.SELF_NUM):
            j = self.player_id * C.SELF_NUM + i
            if self.boards[j] == 0:
                continue
            boards = self.boards.copy()
            pos = []
            idx = j
            for k in range(self.boards[j]):
                idx = (1 + idx) % C.ROOM_NUM
                if idx == j:
                    idx = (1 + idx) % C.ROOM_NUM
                boards[idx] += 1
                pos.append(idx)
                k += 1
            rv_num = 0
            while pos and 2 <= boards[pos[-1]] <= 3:
                idx = pos.pop()
                if self_start <= idx < self_end:
                    break
                rv_num += boards[idx]
                boards[idx] = 0
            op_board_num, self_num = sum(boards[: C.SELF_NUM]), sum(
                boards[C.SELF_NUM :]
            )
            if self.player_id == 0:
                op_board_num, self_num = self_num, op_board_num
            if op_board_num == 0:
                continue
            score = [self.score[0], self.score[1]]
            score[self.player_id] += rv_num
            if self_num == 0:
                rv_num -= op_board_num
            boards[j] = 0
            done = (
                score[self.player_id] >= C.WIN_SCORE or self.curent_round >= C.MAX_ROUND
            )

            s = C.encode_data(1 - self.player_id, self.curent_round + 1, score, boards)
            self.actions[i] = Action(self, i, Rooms.new(s).set_done(done)).set_reward(
                rv_num
            )
        return self.actions

    def to_str(self):
        from common.third_util.export import PtTable

        def u(i, player_id):
            if player_id != self.player_id:
                return 0
            actions = self.get_actions()
            if i in actions:
                return actions[i].get_reward()
            return 0

        p = PtTable().load_from_matrix(
            [
                [f"A{i}:{u(i,0)}" for i in range(6)],
                self.boards[: C.SELF_NUM],
                self.boards[C.SELF_NUM :][::-1],
                [f"B{5-i}:{u(5-i,1)}" for i in range(6)],
            ],
            [f"N{i}" for i in range(6)],
        )
        return str(p) + f"\nscore:{self.score}\n"

    def get_reward(self, actions: List[Action] = None, params=None, **kw):
        r = 0
        c = 1
        for i, a in enumerate(actions):
            ar = a.reward if i % 2 == 0 else -a.reward
            r += ar * c
            c = c * params[0]
        return r

    def get_win_player(self, rewards, *args, **kw):
        if rewards[-1][0] < rewards[-1][1]:
            return 1
        if rewards[-1][0] > rewards[-1][1]:
            return 0
        return -1
