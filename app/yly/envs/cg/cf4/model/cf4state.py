from .cf4action import F4Action
from .constant import C
from common.algo.search.state import State, MctsState
from common.util.export import List, Dict


class F4State(MctsState):

    def __init__(self, state, depth, heights, pos_reward=0):
        super().__init__(state, player_id=depth % 2, depth=depth)
        self.states = [state >> C.SIZE, state & C.MASK_SIZE]
        self.heights: List[int] = heights
        if depth == C.HEIGHT * C.WIDTH:
            self.done = 2
        win_done = self.cal_done()
        if win_done is not None:
            self.done = win_done
        self.pos_reward = self.pos_reward

    @classmethod
    def new(cls, state=0, **kw):
        a, b = state >> C.SIZE, state & C.MASK_SIZE
        heights = []
        depth = 0
        for _ in range(C.WIDTH):
            s: int = (a | b) & C.MASK_HEIGHT
            heights.append(s.bit_length())
            a, b = a >> C.HEIGHT, b >> C.HEIGHT
            depth += heights[-1]
        return super().new(state, heights=heights, depth=depth, **kw)

    def calc_score(self, ct: dict):

        if ct[0][4]:
            self.reward = 1
            return 1
        if ct[1][4]:
            self.reward = -1
            return
        self.reward = self.g.pos_score[0] - self.g.pos_score[1]
        self.reward += (len(ct[0][2]) - len(ct[1][2])) * C.SCORE2
        for i in range(2):
            c = 1 if i == 0 else -1
            for v in ct[i][3].values():
                n: Line = v
                h = 1
                for p in n.pts:
                    if p.value == 2:
                        h = (p.y - self.g.columns[p.x].top) / 2 + 1
                        break
                self.reward += C.SCORE3 * c / h
                self.msgs.append(f"{v}; h:{h}")
        self.msgs.append("reward:%.5f" % self.reward)

    def get_reward(self, actions=None, params=None):
        if self.done == 0:
            return 1
        elif self.done == 1:
            return -1
        return self.pos_reward

    def make_actions(self, *args, **kw) -> Dict[str, F4Action]:
        actions = dict()

        for k in range(C.WIDTH):
            a, b, pos_reward = self.states, self.pos_reward
            h = self.heights[:]
            if h[k] >= C.HEIGHT:
                continue
            if self.player_id == 0:
                a |= C.MASK_POS[k][h[k]]
                pos_reward += C.pos_score(h[k], k)
            else:
                b |= C.MASK_POS[k][h[k]]
                pos_reward -= C.pos_score(h[k], k)
            h[k] += 1
            s = F4State((a << C.SIZE) + b, self.depth + 1, h)
            actions[k] = F4Action(self, k, s)
        return actions

    def to_str(self):
        ret = [["- " if i != 0 else "##"] * C.WIDTH for i in range(C.HEIGHT + 1)]
        for i in range(C.WIDTH):
            for j in range(self.heights[i] - 1, -1, -1):
                if self.states[0] & C.MASK_POS[i][j]:
                    ret[C.HEIGHT - j][i] = f"X "
                elif self.states[1] & C.MASK_POS[i][j]:
                    ret[C.HEIGHT - j][i] = f"O "
                else:
                    break
        ret.append([f"{i}#" for i in range(C.WIDTH)])
        return "\n".join(
            [
                f"{C.HEIGHT-i if C.HEIGHT-i>=0 else ' '}:" + "".join(s)
                for i, s in enumerate(ret)
            ]
            + [str(self.heights)]
            + ["-" * (2 * C.WIDTH)]
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
