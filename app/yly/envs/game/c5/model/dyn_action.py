from common.util.export import TYPE_CHECKING
from .static_action import C5ACtion


class DynAction(C5ACtion):
    def __init__(self, src, action):
        self.src = src
        self.action = action

    def get_dst(self):
        from .dyn_state import DynState

        ret = (
            DynState(
                player_id=1 - self.src.player_id,
            )
            .set_depth(self.src.depth + 1)
            .set_acs(f"{self.src.acs}|{self.action}")
        )
        ret.can_moves = self.src.can_moves.copy()
        ret.can_moves.remove(self.action)
        return ret
