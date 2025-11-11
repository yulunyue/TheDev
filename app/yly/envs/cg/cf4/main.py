from common.util.export import ToolBase, logger, Module, List
from common.algo.export import random_seed, ALgoManage, Algo
from common.third_service.export import CodingGame, uu
from app.yly.envs.cg.cf4.export import (
    F4StateDev as F4State,
    CgMuiltCf4,
    ENV,
    C,
    Kagle,
)


class ToolCf4(ToolBase):

    def prepare(self, args=None):
        self.init_state = F4State.new_shape(0)
        self.al = (
            ALgoManage().set_state(self.init_state).set_record_dir(uu(CgMuiltCf4.name))
        )

    def f1(self):
        self.al.set_players([self.al.mc()], [self.al.mc()]).fight()

    def random(self):
        self.al.actor([self.al.rd()])

    def train(self):
        self.al.train([self.al.mc(100)])

    def debug(self):
        self.dev()

    def dev(self):
        self.random()


if __name__ == "__main__":
    random_seed(3)
    ToolCf4().run()
