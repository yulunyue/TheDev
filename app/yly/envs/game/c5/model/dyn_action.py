from common.util.export import TYPE_CHECKING
from .static_action import C5ACtion


class DynAction(C5ACtion):
    def __init__(self, src, action):
        self.src = src
        self.action = action

    def get_dst(self):
        from .dyn_state import DynState

        return DynState(
            state=f"{self.src.state}|{self.action}",
            player_id=1 - self.src.player_id,
            depth=1 - self.src.player_id,
        )
