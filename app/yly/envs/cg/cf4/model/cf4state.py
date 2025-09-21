from .cf4action import F4Action
from .constant import C
from common.algo.search.state import State, MctsState
from common.util.export import List, Dict


class F4State(MctsState):

    def __init__(self, state):
        self.heights = [0] * C.WIDTH
        self.widths = [0] * C.WIDTH
        self.depth = 0
        self.state = state
        self.point_score = dict()
        # self.pos_reward = 0
        s: int = self.state
        for i in range(C.WIDTH):
            s1: int = s & C.MASK_HEIGHT
            self.widths[i] = s1
            self.heights[i] = s1.bit_length() - 1
            s = s >> C.HEIGHT
            self.depth += self.heights[i]
        self.player_id = self.depth % 2
        if self.depth == C.SIZE:
            self.done = 2

    def make_actions(self):
        actions = []
        for k in range(C.WIDTH):
            if self.heights[k] >= C.HEIGHT - 1:
                continue
            scores = self.get_point_scores(k, self.heights[k])
            next_state = self.__class__.new(self.get_next_state(k))
            if scores[self.player_id][0]:
                next_state.set_done(self.player_id)
            actions.append(F4Action(self, k, next_state))
        return actions

    def calc_score(self, p0, p1, a, extern=0):
        ret = extern
        ci = 0.1
        for j in range(3):
            for i in range(len(p0)):
                if i % 2 == 0:
                    ret += (p0[i][j] + p1[i][j] * 0.1) * ci
                else:
                    ret -= (p1[i][j] + p0[i][j] * 0.1) * ci
                ci *= 0.01
        return ret

    def get_point_scores(self, x, y):
        if (x, y) in self.point_score:
            return self.point_score[x, y]
        scroe0, scroe1 = [0] * 3, [0] * 3
        for ll in C.POINTS[x][y]:
            player_0, player_1 = self.get_pos_line(ll)
            if player_0 > 1:
                scroe0[3 - player_0] += 1
            if player_1 > 1:
                scroe1[3 - player_1] += 1
        self.point_score[x, y] = scroe0, scroe1
        return self.point_score[x, y]

    def get_pos_line(self, l):
        ct = [0, 0, 0]
        pos = [-1] * len(l)
        ret = [0, 0]
        for i, (x, y) in enumerate(l):
            pos[i] = self.get_pos_statu(x, y)
            ct[pos[i]] += 1
            if i >= 3:  # 因为过滤了当前节点 所以只有三个
                ct[pos[i - 3]] -= 1
            if ct[0] + ct[2] == 3 and ct[0] > ret[0]:
                ret[0] = ct[0]
            if ct[1] + ct[2] == 3 and ct[1] > ret[1]:
                ret[1] = ct[1]
        return ret

    def get_pos_statu(self, x, y):
        if y >= self.heights[x]:
            return 2
        if self.widths[x] & C.MASK_POS[y]:
            return 1
        return 0

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

    def calc_cation_reward(self, a):
        depth = 0
        p0, p1 = [], []
        pos_score = C.POS_SCORE[a][self.heights[a]] * C.POS_SCORE_RADIO
        while depth < C.CALC_SCORE_MAX_DEPTH and self.heights[a] + depth < C.HEIGHT - 1:

            scores = self.get_point_scores(a, self.heights[a] + depth)
            if depth == 0 and scores[1 - self.player_id][0]:
                return self.calc_score(p0, p1, a, extern=0.9)
            p0.append(scores[0])
            p1.append(scores[1])
            depth += 1
        if self.player_id == 0:
            return self.calc_score(p0, p1, a, pos_score)
        return self.calc_score(p1, p0, a, pos_score)

    cur_max_action = None

    def get_max_reward(self):
        ret = 0
        for a in self.get_sort_actions():
            reward = self.calc_cation_reward(a.action)
            if reward > ret:
                ret = reward
                self.cur_max_action = a.action
        return ret

    def show(self, info="", title=""):
        self.get_self_reward()
        return super().show(info, title)

    def get_reward(self, **kw):
        if self.reward is not None:
            return self.reward
        if self.done == 0 or self.done == 1:
            self.reward = 1
        else:
            self.reward = self.get_max_reward()
        if self.player_id == 0:
            self.reward = -self.reward
        return self.reward


class F4StateDev(F4State):
    def __init__(self, state):
        self.data = dict()
        super().__init__(state)

    def calc_score(self, p0, p1, a, extern=0):
        ret = super().calc_score(p0, p1, a, extern)
        self.data[a] = f"self:{p0}, op:{p1}, score:{'%.10f'%ret}"
        return ret

    def get_reward(self, **kw):
        ret = super().get_reward()
        self.data["max"] = f"{self.cur_max_action}->{'%.10f'%ret}"
        return ret
