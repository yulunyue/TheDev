from common.algo.export import Action
from app.yly.envs.cg.tic_toc.constant import C


class TtAction(Action):
    def __init__(self, src, action, dst=None):
        from app.yly.envs.cg.tic_toc.model.ttstate9 import TtState

        self.src: TtState = src
        self.dst: TtState = dst
        self.action: int = action
