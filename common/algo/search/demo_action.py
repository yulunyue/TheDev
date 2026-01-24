from .action import Action


class DemoAction(Action):
    def set_next_state(self, state, r):
        self.next_state = state
        self.reward = r
        return self

    def do(self):
        self.dst = self.next_state
        self.dst.state = f"{self.src.state}->{self.action}->{self.dst.state}"
        return self

    def undo(self):
        self.dst.state = ""
        return self
