from .static_state import StateStatic
from .dyn_action import DynAction


class DynState(StateStatic):

    def get_action(self, pos):
        return DynAction(self, pos)
