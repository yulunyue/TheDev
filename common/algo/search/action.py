from common.util.export import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import State


class Action:
    check_info = None

    def __init__(self, src, action, dst=None):
        self.action = action
        self.src: State = src
        self.dst: State = dst
        self.data = dict()

    @property
    def title(self):
        return self.action

    @property
    def key(self):
        return f"{self.src.state}->{self.action}"

    def get_dst(self):
        return self.dst

    def get_data(self, key, default_value):
        return self.data.get(key, default_value)

    def set_data(self, **kw):
        self.data.update(kw)
        return self

    p = None

    def set_p(self, p):
        self.p = p
        return self

    def set_reward(self, reward):
        self.reward = reward
        return self

    def get_reward(self, **kwargs):
        return self.reward  # 值越大越好,返回当前行为的优势

    def get_src_reward(self, actions: List["Action"], **kw):
        return self.get_reward()

    def show(self, msg=None):
        ret = f"src:{self.src.state}, dst:{self.dst.state}, action:{self.action}"
        if self.data:
            ret += f", data:{self.data}"
        if msg:
            ret += f", msg:{msg}"
        reward = getattr(self, "reward", None)
        if reward is not None and self.reward > 0:
            ret += f", rwin:{self.reward}"
        elif reward is not None and self.reward < 0:
            ret += f", rlos:{self.reward}"
        return ret

    def show_best_actions(self):
        a = self
        ret = []
        while a:
            ret.append(a.show())
            ret.append(a.get_dst().show())
            a = a.get_dst().get_action()
        return "\n".join(ret)

    def do(self):
        """ """
        pass

    def undo(self):
        pass

    def get_dqn_network_params(self, acs: List["Action"]):
        """
        rewards, dones, q_values, max_next_q_values
        """
        from common.third_util.ml.torch_util import torch
        from common.third_util.ml.np_util import np

        states = torch.tensor(np.array([a.src.state for a in acs]), dtype=torch.float)
        actions = torch.tensor([a.action for a in acs]).view(-1, 1)
        rewards = torch.tensor([a.reward for a in acs], dtype=torch.float).view(-1, 1)
        next_states = torch.tensor(
            np.array([(a.dst.state) for a in acs]), dtype=torch.float
        )
        dones = torch.tensor([a.dst.done for a in acs], dtype=torch.float).view(-1, 1)

        # 下个状态的最大Q值

        return states, actions, rewards, dones, next_states
