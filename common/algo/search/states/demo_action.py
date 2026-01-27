from .action import Action


class DemoAction(Action):
    reward = None

    def do(self):
        self.set_reward(self.dst.r)
        return self

    def undo(self):
        return self
