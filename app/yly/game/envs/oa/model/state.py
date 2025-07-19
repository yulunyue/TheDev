from common.algo.search.state import State
from common.algo.base.bin_util import decode_data, encode_data
from common.util.export import List


class Rooms(State):
    ROOM_NUM = 12
    OR_NUM = 4
    MASK_POSS = [1] + [3] * ROOM_NUM
    STATE_MAP = dict()

    def __init__(self, state=None, boards=None, player_id=0, depth=0):
        self.boards: List[int] = boards
        super().__init__(state, player_id, depth)

    @staticmethod
    def new(state) -> "Rooms":
        if state not in Rooms.STATE_MAP:
            player_id, *boards = decode_data(state, Rooms.MASK_POSS)
            Rooms.STATE_MAP[state] = Rooms(state, boards, player_id=player_id)
        ret = State()
        return ret

    def reset(self):
        self.roomall = [4] * self.ROOM_NUM
        self.actions = list(range(6))
        return self

    def set_rooms(self, rooms):
        for i, v in enumerate(rooms):
            self.roomall[i] = v
        return self

    def get_action(self):
        for a in self.actions:
            if self.roomall[a]:
                return a

    def do_action(self, action):
        for i in range(self.roomall[action]):
            self.roomall[(action + i + 1) % self.ROOM_NUM] += 1
        self.roomall[action] = 0
        return self
