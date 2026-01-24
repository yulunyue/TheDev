from .action import Action


class DemoAction(Action):
    reward = None

    def set_next_state(self, state):
        self.next_state = state
        return self

    def do(self):
        self.dst = self.next_state
        self.set_reward(self.dst.r)
        self.dst.state = f"{self.src.state}-{self.action}"
        return self

    def undo(self):
        return self
