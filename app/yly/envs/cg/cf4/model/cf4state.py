from .cf4action import F4Action
from .constant import C
from common.algo.search.state import State, MctsState
from common.util.export import List, Dict


class F4State(MctsState):

    def __init__(self, state, heights=None):
        super().__init__(state)
        if heights is None:
            self.init_from_state()
        else:
            self.heights = heights
        if self.depth == C.SIZE and self.done is None:
            self.done = 2

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
            self.depth += self.heights[-1]
        self.player_id = self.depth % 2
        for i in range(C.WIDTH):
            done, player_info = self.get_player_action_info(i)
            if done == 1 or done == 0:
                self.done = done
            # self.data[i] = player_info

    def get_reward(self, **kw):
        # for i in range(C.WIDTH):
        #     pass
        if self.done == 0:
            self.reward = 1
        elif self.done == 1:
            self.reward = -1
        else:
            # self.reward = self.pos_reward * C.POS_SCORE_RADIO
            self.reward = 0
        return self.reward

    def get_point_info(self, x, y) -> tuple[list[int], list[int]]:
        player0, player1 = [0, 0, 0], [0, 0, 0]
        for i, ll in enumerate(C.POINTS[x][y]):
            max_l = self.get_pos_line(ll)
            if max_l[0] > 1:
                player0[max_l[0] - 1] += 1
            if max_l[1] > 1:
                player1[max_l[1] - 1] += 1
        return player0, player1

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
        done, player_point_info = self.get_player_action_info(k)
        if done != -1:
            return done, None
        mask = self.widths[k]
        mask |= C.MASK_POS[self.heights[k] + 1]
        if self.player_id == 0:
            mask &= C.HEIGHT_CLEAR[self.heights[k]]
        state = (self.state & C.WIDTH_MASK[k]) | (mask << k * C.HEIGHT)
        s = F4State.new(state)
        return done, s

    def get_player_action_info(self, k):
        if self.heights[k] >= C.HEIGHT - 1:
            return None, []
        player_point_info = self.get_point_info(k, self.heights[k])
        if player_point_info[self.player_id][2]:
            return self.player_id, player_point_info
        return -1, player_point_info

    def make_actions(self, *args, **kw) -> Dict[str, F4Action]:
        actions = dict()
        for k, mask in enumerate(self.widths):
            done, s = self.get_next_state(k)
            if done == 0 or done == 1:
                self.done = done
                return
            if s is None:
                continue
            actions[k] = F4Action(self, k, s)
        return actions

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
