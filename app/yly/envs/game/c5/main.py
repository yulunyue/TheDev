from common.util.export import ToolBase, logger
from common.algo.export import ALgoManage
from .state import State, C


class C5Tool(ToolBase):
    def prepare(self, *args, **kw):
        self.s = State.new()
        self.al = ALgoManage().set_state(self.s)

        return super().prepare(*args, **kw)

    def view1(self):
        logger.debug(self.s.show())
        for a in self.s.get_sort_actions():
            logger.debug(a.show())
            logger.debug(a.get_dst().show())

    def view3(self):
        a = State.new(0x40200000000000000).get_action(25)
        self.logger.debug(a.show())
        self.logger.debug(a.get_dst().show())

    def view_state(self):
        logger.debug(State.new(0x4000).show())

    def view_random(self):
        s = self.s
        logger.debug(s.show())
        idx = 0
        while not s.game_over():
            a = s.get_random_action()
            logger.debug(idx)
            logger.debug(a.show())
            s = a.get_dst()
            logger.debug(s.show())
            idx += 1

    def actor(self):
        self.al.actor([self.al.ab(5), self.al.ab(5)])

    def mc(self):
        a = self.al.mc().search(self.s)
        logger.debug(a.show())
        logger.debug(a.get_dst().show())

    def mcactor(self):
        logger.info(self.al.actor([self.al.mc()]))

    def debug(self):
        self.view3()


if __name__ == "__main__":
    C5Tool().run()
