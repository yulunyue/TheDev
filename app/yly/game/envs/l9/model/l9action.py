from common.algo.search.state import Action
from app.yly.game.envs.l9.constant import C


class L9Action(Action):

    def __init__(self, src, dst):
        super().__init__(src, None, dst=dst)

    def load(self, method, src_key=None, dst_key=None, remove_key=None):
        self.method = method
        self.src_key = src_key
        self.dst_key = dst_key
        self.remove_key = remove_key
        self.action = self.to_cg_str()
        return self

    def to_cg_str(self) -> str:
        if self.method == C.PLACE:
            if self.remove_key:
                return f"{C.PLACE};{self.src_key};{self.remove_key}"
            return f"{C.PLACE};{self.src_key}"
        return ""

    def get_reward(self, **kwargs):
        return 0
