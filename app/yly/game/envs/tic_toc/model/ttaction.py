from common.algo.export import Action
from app.yly.game.envs.tic_toc.constant import C


class TtAction(Action):
    def get_reward(self, player_id, **kwargs):
        value = 0
        if self.dst.done == 1 or self.dst.done == 2:
            value = C.MAX_SCORE
        return value if player_id == self.dst.player_id else -value

    def __repr__(self):
        y, x = self.action // 9, self.action % 9
        return f"action->a:{self.action} y:{y} x:{x}"
