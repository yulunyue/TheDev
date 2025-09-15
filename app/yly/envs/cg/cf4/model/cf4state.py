from .cf4action import F4Action
from .constant import C
from common.algo.search.state import State, MctsState
from common.util.export import List, Dict


class F4State(MctsState):
    def __init__(self, state, heights, depth, pos_reward):
        super().__init__(state, depth % 2, depth)
        self.states = [self.state >> C.SIZE, self.state & C.MASK_SIZE]
        self.heights: List[int] = heights
        if depth == C.HEIGHT * C.WIDTH:
            self.done = 2
        win_done = self.cal_done()
        if win_done is not None:
            self.done = win_done
        self.pos_reward = pos_reward

    @classmethod
    def new(cls, state=0, heights=None, depth=0, pos_reward=0):
        a, b = state >> C.SIZE, state & C.MASK_SIZE
        if heights is None:
            heights = []
            depth = 0
            pos_reward = 0
            for _ in range(C.WIDTH):
                s: int = (a | b) & C.MASK_HEIGHT
                heights.append(s.bit_length())
                a, b = a >> C.HEIGHT, b >> C.HEIGHT
                depth += heights[-1]
        return super().new(state, heights=heights, depth=depth, pos_reward=pos_reward)

    def get_reward(self, actions=None, params=None):
        if self.done == 0:
            self.reward = 1
        elif self.done == 1:
            self.reward = -1
        else:
            self.reward = self.pos_reward * C.POS_SCORE_RADIO
        return self.reward

    def make_actions(self, *args, **kw) -> Dict[str, F4Action]:
        actions = dict()

        for k in range(C.WIDTH):
            a, b = self.states
            pos_reward = self.pos_reward
            h = self.heights[:]
            if h[k] >= C.HEIGHT:
                continue
            if self.player_id == 0:
                a |= C.MASK_POS[k][h[k]]
                pos_reward += C.POS_REWARD[k][h[k]]
            else:
                b |= C.MASK_POS[k][h[k]]
                pos_reward -= C.POS_REWARD[k][h[k]]
            h[k] += 1
            s = F4State(
                (a << C.SIZE) + b,
                depth=self.depth + 1,
                heights=h,
                pos_reward=pos_reward,
            )
            actions[k] = F4Action(self, k, s)
        return actions

    def to_str(self):
        ret = [["- " if i != 0 else "##"] * C.WIDTH for i in range(C.HEIGHT + 1)]
        for i in range(C.WIDTH):
            for j in range(self.heights[i] - 1, -1, -1):
                if self.states[0] & C.MASK_POS[i][j]:
                    ret[C.HEIGHT - j][i] = f"O "
                elif self.states[1] & C.MASK_POS[i][j]:
                    ret[C.HEIGHT - j][i] = f"X "
                else:
                    break
        ret.append([f"{i}#" for i in range(C.WIDTH)])
        return "\n".join(
            [
                f"{C.HEIGHT-i if C.HEIGHT-i>=0 else ' '}:" + "".join(s)
                for i, s in enumerate(ret)
            ]
        )

    def get_action(self, actions):
        if isinstance(actions, str):
            actions = int(actions)
        return super().get_action(actions)

    def cal_done(self):
        s = self.states[1 - self.player_id]
        for pos in [1, C.HEIGHT - 1, C.HEIGHT, C.HEIGHT + 1]:
            s1 = s & (s >> pos)
            if s1 & (s1 >> (pos * 2)):
                return 1 - self.player_id

    def check_cg(self, state, last_state: State = None, **kw):
        if last_state and last_state.state != state[0]:
            raise Exception(f"{self.show()}\n{state}")
        if state[1] != self.state:
            raise Exception(f"{self.show()}\n{state}")
