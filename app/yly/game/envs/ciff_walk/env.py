from common.algo.export import State, Action
from common.util.export import logger
from typing import Dict
import numpy as np

ACTIONS = [[-1, 0], [1, 0], [0, -1], [0, 1]]
ACS = ["^", "v", "<", ">"]


class CfEnv:
    ncol = 12
    nrow = 4
    INIT_SATTE = 36

    def get_expects(self):
        return [[34, 3], [24, 3], [35, 1], [36, 0]]

    def do_action(self, state, i):
        a = ACTIONS[i]
        y, x = state // self.ncol, state % self.ncol
        next_y = min(max(y + a[0], 0), self.nrow - 1)
        next_x = min(max(x + a[1], 0), self.ncol - 1)
        reward, done = -1, 0
        next_state = next_y * 12 + next_x
        if next_y == self.nrow - 1 and next_x > 0:
            done = 1
            if next_x != self.ncol - 1:
                reward = -100
        return next_state, reward, done

    def to_str(self, name="p"):
        ret = [""]

        def vt(info):
            ret.append(f"----{info}----")
            for i in range(self.nrow):
                tmp = []
                for j in range(self.ncol):
                    s = CfState.new_one(i * ENV.ncol + j)
                    if info == "value":
                        tmp.append("%6.6s" % ("%.3f" % s.value))
                    elif info == "p":
                        if s.done:
                            t = "EEEE" if s.state == 47 else "****"
                        else:
                            actions = list(s.get_actions().values())
                            max_value = max([v.value for v in actions])
                            t = [
                                ACS[a.action] if a.value == max_value else "o"
                                for a in actions
                            ]
                        tmp.append("".join(t))
                ret.append(" ".join(tmp))

        vt(name)
        return "\n".join(ret)


ENV = CfEnv()


class CfState(State):

    @classmethod
    def new_one(cls, state=ENV.INIT_SATTE) -> "CfState":
        return cls.new_state(state)

    def get_actions_all(self):
        return list(range(len(ACTIONS)))

    def gen_action(self, i):
        next_state, reward, done = ENV.do_action(self.state, i)
        # logger.info([self.state, i, next_state])
        return (
            Action(self, i, CfState.new_one(state=next_state).set_done(done))
            .set_value(0)
            .set_p(0.25)
            .set_reward(reward)
        )
