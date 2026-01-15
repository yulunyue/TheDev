from .static_state import StateStatic
from .dyn_action import DynAction


class DynState(StateStatic):
    acs = ""

    def get_action(self, pos):
        return DynAction(self, pos)

    def set_acs(self, acs):
        self.acs = acs
        return self
