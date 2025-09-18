from .cf4action import F4Action
from .constant import C
from common.algo.search.state import State, MctsState
from common.util.export import List, Dict


class F4State(MctsState):

    def __init__(self, state):
        super().__init__(state)
        self.init_from_state()

    def init_from_state(self):
        self.heights = [0] * C.WIDTH
        self.widths = [0] * C.WIDTH
        self.depth = 0
        # self.pos_reward = 0
        s: int = self.state
        for i in range(C.WIDTH):
            s1: int = s & C.MASK_HEIGHT
            self.widths[i] = s1
            self.heights[i] = s1.bit_length() - 1
            s = s >> C.HEIGHT
            self.depth += self.heights[i]
        self.player_id = self.depth % 2
        self.actions = []
        for k in range(C.WIDTH):
            if self.heights[k] >= C.HEIGHT - 1:
                continue
            scores = self.get_point_scores(k)
            state = self.get_next_state(k)
            self.actions.append(F4Action(self, k, state, scores))

    def get_point_scores(self, x, depth=0):
        scroe0, scroe1 = [0] * 3, [0] * 3
        y = self.heights[x] + depth
        for ll in C.POINTS[x][y]:
            player_0, player_1 = self.get_pos_line(ll)
            if player_0 > 1:
                scroe0[3 - player_0] += 1
            if player_1 > 1:
                scroe1[3 - player_1] += 1
        return scroe0, scroe1

    def get_pos_line(self, l):
        ct = [0, 0, 1]
        pos = [0] * len(l)
        ret = [0, 0]
        for i, (x, y) in enumerate(l):
            pos[i] = self.get_pos_statu(x, y)
            ct[pos[i]] += 1
            if i >= 4:
                ct[pos[i - 4]] -= 1
            if pos[i] != 2 and ct[pos[i]] + ct[2] == 4:
                ret[pos[i]] = max(ret[pos[i]], ct[pos[i]])
        return ret

    def get_pos_statu(self, x, y):
        if y >= self.heights[x]:
            return 2
        if self.widths[x] & C.MASK_POS[y]:
            return 1
        return 0

    def get_done(self):
        return self.done

    def get_next_state(self, k):

        mask = self.widths[k]
        mask |= C.MASK_POS[self.heights[k] + 1]
        if self.player_id == 0:
            mask &= C.HEIGHT_CLEAR[self.heights[k]]
        state = (self.state & C.WIDTH_MASK[k]) | (mask << k * C.HEIGHT)
        return state

    def to_str(self):
        ret = [["- " if i != 0 else "##"] * C.WIDTH for i in range(C.HEIGHT)]
        s = self.state
        for i in range(C.WIDTH):
            for j in range(self.heights[i] - 1, -1, -1):
                if s & C.MASK_POS[j]:
                    ret[C.HEIGHT - j - 1][i] = f"X "
                else:
                    ret[C.HEIGHT - j - 1][i] = f"0 "
            s = s >> C.HEIGHT
        ret.append([f"{i}#" for i in range(C.WIDTH)])
        return "\n".join(
            [
                f"{C.HEIGHT-i-1 if C.HEIGHT-i-1>=0 else ' '}:" + "".join(s)
                for i, s in enumerate(ret)
            ]
        )

    def get_action(self, actions):
        if isinstance(actions, str):
            actions = int(actions)
        return super().get_action(actions)

    def check_cg(self, state, last_state: State = None, **kw):
        if last_state and last_state.state != state[0]:
            raise Exception(f"{self.show()}\n{state}")
        if state[1] != self.state:
            raise Exception(f"{self.show()}\n{state}")
