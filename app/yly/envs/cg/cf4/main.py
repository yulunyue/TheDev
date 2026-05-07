from common.util.export import ToolBase, logger, Module, List, log
from common.algo.export import random_seed, ALgoManage, Algo
from common.third_service.get_service import CodingGame, uu
from app.yly.envs.cg.cf4.export import (
    F4StateDev as F4State,
    CgMuiltCf4,
    ENV,
    C,
    Kagle,
)


class ToolCf4(ToolBase):

    def prepare(self, args=None):
        self.init_state: F4State = F4State.new_shape(0)
        self.al = (
            ALgoManage().set_state(self.init_state).set_record_dir(uu(CgMuiltCf4.name))
        )

    def f1(self):
        self.al.set_players([self.al.mc()], [self.al.mc()]).fight()

    def random(self):
        self.al.actor([self.al.rd()])

    def train(self):
        self.al.train([self.al.mc(100)])

    def dev2(self):
        s = self.init_state
        logger.debug(s.show())
        for v in [0]:
            a = s.get_action(v)
            s = a.get_dst()
            logger.debug(a.show())
            logger.debug(s.show())

    def dev1(self):
        log.debug(self.init_state.show())
        for a in self.init_state.get_sort_actions():
            log.debug(a.show())
            log.debug(a.get_dst().show())

    def dev(self):
        self.random()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    random_seed(3)
    ToolCf4().run()
