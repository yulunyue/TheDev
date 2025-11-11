from .cf4action import F4Action
from .constant import C
from common.algo.search.state import AbState
from common.util.export import List, Dict, logger
from .env import ENV


class F4State(AbState):

    def __init__(self, state):
        super().__init__(state)
        ENV.set_state(state)
        self.depth = ENV.step
        self.player_id = self.depth % 2

    @classmethod
    def new_shape(cls, shape):
        ENV.set_shape(shape)
        return cls.new(ENV.INIT_MASK)

    def make_actions(self):
        actions = []
        op_win_actions = []
        for k in range(C.WIDTH):
            if self.heights[k] >= C.HEIGHT - 1:
                continue
            scores = self.get_point_scores(k, self.heights[k])
            next_state: F4State = self.__class__.new(self.get_next_state(k))
            a = F4Action(self, k, next_state)
            if scores[self.player_id][0]:
                next_state.set_done(self.player_id)
                return [a]
            elif scores[1 - self.player_id][0]:
                op_win_actions = [a]
            else:
                actions.append(F4Action(self, k, next_state))
        return op_win_actions if op_win_actions else actions

    def calc_score(self, p, a):
        ret = 0
        for i, v in enumerate(p):
            ret += v * C.SCORES[self.player_id][i]
        return ret  # C.ACTION_SCORE[a]

    def get_point_scores(self, x, y):
        if (x, y) in self.point_score:
            return self.point_score[x, y]
        self.point_score[x, y] = self.calc_point_scroes(x, y)
        return self.point_score[x, y]

    def calc_point_scroes(self, x, y):
        scroe0, scroe1 = [0] * 3, [0] * 3
        for j, ll in enumerate(C.POINTS[x][y]):
            player_0, player_0num, player_1, player_1num = self.get_pos_line(ll)
            if player_0 > 1:
                scroe0[3 - player_0] += player_0num
            if player_1 > 1:
                scroe1[3 - player_1] += player_1num
        return scroe0, scroe1

    def get_pos_line(self, l):
        ct = [0, 0, 0]
        pos = [-1] * len(l)
        ret = [0, 0, 0, 0]

        def u(i):
            j = i * 2
            if ct[i] + ct[2] == 3 and ct[i]:
                if ct[i] > ret[j]:
                    ret[j] = ct[i]
                    ret[j + 1] = 1
                elif ct[i] == ret[j]:
                    ret[j + 1] += 1

        for i, (x, y) in enumerate(l):
            pos[i] = self.get_pos_statu(x, y)
            ct[pos[i]] += 1
            if i >= 3:  # 因为过滤了当前节点 所以只有三个
                ct[pos[i - 3]] -= 1
            u(0)
            u(1)
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

    def calc_action_reward(self, a):
        p0, p1 = self.get_point_scores(a, self.heights[a])
        return self.calc_score(p0 + p1, a)

    def get_max_reward(self):
        ret = 0
        for a in self.get_sort_actions():
            reward = self.calc_action_reward(a.action)
            if reward > ret:
                ret = reward
        return ret

    def get_reward(self):
        if self.reward is not None:
            return self.reward
        self.reward = self.get_max_reward()
        if (
            self.player_id == 1
        ):  # 如果当前执行玩家是先手，表示该状态为后手玩家的执行结果，后手玩家优势值越小优势越大，所以取反
            self.reward = -self.reward
        return self.reward


class F4StateDev(F4State):
    def __init__(self, state):
        self.scores_record = dict()
        self.data = dict()
        super().__init__(state)

    def calc_score(self, p, a):
        ret = super().calc_score(p, a)
        self.scores_record[a] = [
            ret,
            f"{a}->p:{p}, r:{ret}",
            a,
        ]
        return ret

    def show(self, info=None, title=""):
        self.get_reward()
        self.score2 = sorted(self.scores_record.values(), reverse=True)
        if info is None:
            info = []
        return super().show(info=info + [v[1] for v in self.score2], title=title)

    def check_cg(self, stdout, summary):
        if stdout == "-2":
            logger.info(summary)
            return True
        return False
