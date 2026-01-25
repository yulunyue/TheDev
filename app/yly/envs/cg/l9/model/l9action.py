from common.algo.search.states.state import Action
from app.yly.envs.cg.l9.constant import C


class L9Action(Action):

    def __init__(self, src, dst):
        from app.yly.envs.cg.l9.model.l9state import L9State

        self.src: L9State = src
        self.dst: L9State = dst

    def load(
        self,
        method,
        src_key=None,
        dst_key=None,
        remove_key=None,
        board=None,
        done=False,
    ):
        self.method = method
        self.src_key = src_key
        self.dst_key = dst_key
        self.remove_key = remove_key
        self.action = self.to_cg_str()
        return self

    def to_cg_str(self) -> str:
        a = self.method + ";" + self.src_key
        if self.dst_key:
            a += ";" + self.dst_key
        if self.remove_key:
            a += ";" + self.remove_key
        return a

    def get_reward(self, **kwargs):
        return 0
