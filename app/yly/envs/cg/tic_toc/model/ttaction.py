from common.algo.export import Action
from app.yly.game.envs.tic_toc.constant import C


class TtAction(Action):
    def __init__(self, src, action, dst=None):
        from app.yly.game.envs.tic_toc.model.ttstate import TtState

        self.src: TtState = src
        self.dst: TtState = dst
        self.action: int = action

    def __repr__(self):
        y, x = self.action // 9, self.action % 9
        return f"{x},{y}"
