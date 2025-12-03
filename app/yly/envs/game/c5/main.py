from common.util.export import ToolBase, logger, log
from common.algo.export import ALgoManage, random_seed
from .state import State, C


class C5Tool(ToolBase):
    def prepare(self, *args, **kw):
        self.s = State.new()
        self.al = ALgoManage().set_state(self.s)
        return super().prepare(*args, **kw)

    def view1(self):
        log.debug(self.s.show())
        for a in self.s.get_sort_actions():
            log.debug(a.show())
            log.debug(a.get_dst().show())

    def view3(self):
        a = State.new(0x40200000000000000).get_action(25)
        self.logger.debug(a.show())
        self.logger.debug(a.get_dst().show())

    def view_state(self):
        logger.debug(State.new(0x4000).show())

    def random(self):
        s = self.s
        log.debug(s.show())
        idx = 0
        while not s.game_over():
            a = s.get_random_action()
            log.debug(f"turn:{idx}")
            log.debug(a.show())
            s = a.get_dst()
            log.debug(s.show())
            idx += 1

    def actor(self):
        self.al.actor([self.al.ab(5), self.al.ab(5)])

    def mc(self):
        a = self.al.mc().search(self.s)
        logger.debug(a.show())
        logger.debug(a.get_dst().show())

    def mcactor(self):
        log.info(self.al.actor([self.al.mc()]))

    def dev(self):
        self.mcactor()

    def debug(self):
        self.view3()


if __name__ == "__main__":
    random_seed(4)
    C5Tool().run()
