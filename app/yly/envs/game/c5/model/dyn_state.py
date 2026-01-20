from .static_state import StateStatic, BoardC5
from .dyn_action import DynAction


class DynState(StateStatic):
    init_state = ""

    def get_action(self, pos):
        return DynAction(self, pos)
