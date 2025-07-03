from common.algo.export import State, Action, MctsNode
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
        return [[2, 10, [3]], [2, 0, [3, 0]], [2, 11, [1]], [3, 0, [0]]]

    def get_yx(self, state):
        return state // self.ncol, state % self.ncol

    def do_action(self, state, i):
        a = ACTIONS[i]
        y, x = self.get_yx(state)
        next_y = min(max(y + a[0], 0), self.nrow - 1)
        next_x = min(max(x + a[1], 0), self.ncol - 1)
        reward, done = -1, 0
        next_state = next_y * 12 + next_x
        if next_y == self.nrow - 1 and next_x > 0:
            done = 1
            if next_x != self.ncol - 1:
                reward = -100
        return next_state, reward, done

    def to_str(self, tp="p"):
        ret = [""]

        ret.append(f"----{tp}----")
        for i in range(self.nrow):
            tmp = []
            for j in range(self.ncol):
                s = CfState.new_one(i * ENV.ncol + j)

                if s.done:
                    t = "EEEE" if s.state == 47 else "****"
                    if tp == "p":
                        s2 = "".join(t)
                    else:
                        s2 = "%6.6s" % ("%.3f" % 0)
                else:
                    actions = list(s.get_actions().values())
                    max_value = max([v.value for v in actions])
                    t = [
                        ACS[a.action] if a.value == max_value else "o" for a in actions
                    ]
                    if tp == "p":
                        s2 = "".join(t)
                    else:
                        s2 = "%6.6s" % ("%.3f" % max_value)
                tmp.append(s2)
            ret.append(" ".join(tmp))
        ret.append("--------")
        return "\n".join(ret)


ENV = CfEnv()


class CfState(MctsNode):

    @classmethod
    def new_one(cls, state=ENV.INIT_SATTE) -> "CfState":
        return cls.new_state(state)

    def get_actions_all(self):
        return list(range(len(ACTIONS)))

    def gen_action(self, i):
        next_state, reward, done = ENV.do_action(self.state, i)
        # logger.info([self.state, i, next_state])
        a = (
            Action(self, i, CfState.new_one(state=next_state).set_done(done))
            .set_value(0)
            .set_reward(reward)
        )
        a.visite_num = 0
        return a

    def reset_env(self):

        for v in list(CfState.STATE_STORE.values()):
            v.reset()
            for a in v.get_actions().values():
                a.set_value(0)
                a.visite_num = 0
        return self

    def __repr__(self):
        y, x = ENV.get_yx(self.state)
        a = ",".join(["%.2f" % a.value for a in self.get_actions().values()])
        return f"[y:{y} x:{x} a:{a}]"
