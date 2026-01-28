from .action import Action


class DemoAction(Action):
    reward = None

    def do(self):
        self.reward = self.dst.r
        return self.dst
