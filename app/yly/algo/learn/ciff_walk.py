from common.algo.learn.dqn import State, Action
from common.util.export import logger
from typing import Dict
import numpy as np

ACTIONS = [[-1, 0], [1, 0], [0, -1], [0, 1]]
ACS = ["^", "v", "<", ">"]


class CfState(State):
    ncol = 12
    nrow = 4
    INIT_SATTE = 36

    @classmethod
    def new_one(cls, state=36, done=None, reward=0) -> "CfState":
        return cls.new_state(state).set_done(done).set_reward(reward)

    def get_nexts(self, *args):
        return self.actions

    def get_actions_all(self):
        return list(range(len(ACTIONS)))

    def gen_action(self, i):
        a = ACTIONS[i]
        y, x = self.state // self.ncol, self.state % self.ncol
        next_y = min(max(y + a[0], 0), self.nrow - 1)
        next_x = min(max(x + a[1], 0), self.ncol - 1)
        reward, done = -1, None
        next_state = next_y * 12 + next_x
        if y == self.nrow - 1 and x > 0:
            next_state, reward, done = self.state, 0, 1
        elif next_y == self.nrow - 1 and next_x > 0:
            done = 1
            if next_x != self.ncol - 1:
                reward = -100
        # logger.info([self.state, i, next_state])
        return (
            Action(self, i, CfState.new_one(state=next_state, done=done))
            .set_p(0.25)
            .set_reward(reward)
        )

    def get_actions(self, depth=1, **kw) -> Dict[str, Action]:
        if self.actions is not None:
            return self.actions
        return self.make_actions()

    @classmethod
    def all_state_key(self):
        return [i for i in range(self.ncol * self.nrow)]

    @classmethod
    def to_str(cls):
        ret = [""]

        def vt(info):
            ret.append(f"----{info}----")
            for i in range(CfState.nrow):
                tmp = []
                for j in range(CfState.ncol):
                    s = CfState.new_state(i * CfState.ncol + j)
                    if info == "value":
                        tmp.append("%6.6s" % ("%.3f" % s.value))
                    elif info == "p":
                        if s.done is not None:
                            t = "EEEE" if s.state == 35 else "****"
                        else:
                            t = [
                                ACS[v.action] if v.p > 0 else "o"
                                for v in s.get_actions().values()
                            ]
                        tmp.append("".join(t))
                ret.append(" ".join(tmp))

        vt("value")
        vt("p")
        return "\n".join(ret)
