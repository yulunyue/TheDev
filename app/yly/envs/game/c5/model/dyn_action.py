from common.util.export import TYPE_CHECKING
from .static_action import C5ACtion


class DynAction(C5ACtion):

    def do(self):
        if self.dst is not None:
            return self
        from .dyn_state import DynState

        self.dst = DynState(
            player_id=1 - self.src.player_id,
        ).set_depth(self.src.depth + 1)
        self.dst.state = (
            f"{self.src.state}|{self.action}" if self.src.state else f"{self.action}"
        )
        obs = self.src.board.put_chess(self.action, self.src.player_id + 1)
        self.dst.can_moves = list(self.src.board.can_use)
        self.set_obs(obs)
        return self

    def undo(self):
        self.src.board.change_chess_statu(self.action, 0)
