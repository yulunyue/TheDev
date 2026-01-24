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
        return self

    def undo(self):
        return self
