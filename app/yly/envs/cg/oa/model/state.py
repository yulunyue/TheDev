from common.algo.search.state import State, Action
from common.algo.search.state import Action
from common.util.export import List
from app.yly.envs.cg.oa.model.constant import C


class Rooms(State):

    STATE_MAP = dict()

    def __init__(self, state=None, boards=None, player_id=0, depth=0):
        self.boards: List[int] = boards
        super().__init__(state, player_id, depth)

    @staticmethod
    def new(state) -> "Rooms":
        if state not in Rooms.STATE_MAP:
            player_id, *boards = C.decode_data(state)
            Rooms.STATE_MAP[state] = Rooms(state, boards, player_id=player_id)
        return Rooms.STATE_MAP[state]

    @staticmethod
    def new_room(play_id, boards):
        return Rooms.new(C.encode_data(play_id, boards))

    def make_actions(self, *args, **kw):
        self.actions = dict()
        self_start = self.player_id * C.SELF_NUM
        self_end = self_start + C.SELF_NUM
        self.op_board_num = (
            sum(self.boards[: C.SELF_NUM])
            if self.player_id == 1
            else sum(self.boards[C.SELF_NUM :])
        )
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

            if self.op_board_num == rv_num:
                continue
            boards[j] = 0
            self.actions[i] = Action(
                self, i, Rooms.new_room(1 - self.player_id, boards)
            ).set_reward(rv_num if self.player_id == 0 else -rv_num)
        return self.actions

    def to_str(self):
        s = []
        for i in range(2):
            ts = []
            for j in range(C.SELF_NUM):
                if i == 0:
                    k = C.ROOM_NUM - j - 1
                else:
                    k = j
                ts.append(str(self.boards[k]))
            s.append(" ".join(ts))
        return "\n".join(s)

    def get_reward(self, actions: List[Action] = None, **kw):
        r = 0
        for i, a in enumerate(actions):
            r += a.reward
        return r

    def get_win_player(self, rewards, *args, **kw):
        if rewards[-1][0] < rewards[-1][1]:
            return 1
        if rewards[-1][0] > rewards[-1][1]:
            return 0
        return -1
