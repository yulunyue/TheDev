from common.util.export import ToolBase, logger
from common.algo.export import ALgoManage
from .state import State


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

    def mc(self):
        a = self.al.mc().search(self.s)
        logger.debug(a.show())
        logger.debug(a.get_dst().show())

    def mcactor(self):
        logger.info(self.al.actor([self.al.mc()]))

    def test(self):
        self.mc()


if __name__ == "__main__":
    C5Tool().run()
