from .data import Data


class MprAlgo:
    def __init__(self):
        self.mode = ""
        self.histroy = []

    def get_power(self):
        return 100

    def execute(self, **param):
        self.param = param
        self.param.update(power=self.get_power())
        d = Data().set_history(self.histroy).set_data(**self.param)
        return d.next_checkpoint_x, d.next_checkpoint_y, self.get_power()

    def set_op_pos(self, op):
        self.opponent_x, self.opponent_y = op
        return self

    def get_param(self):
        return self.param
