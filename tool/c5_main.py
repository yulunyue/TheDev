from common.util.export import ToolBase, logger, log, time, File
from common.algo.export import ALgoManage, random_seed, Algo
from app.yly.envs.game.c5.state import State, C
from app.yly.envs.game.c5.case import CASE
from app.yly.envs.game.c5.constant import load


class C5Tool(ToolBase):
    def prepare(self):
        load(8, 8, 5)
        self.s = State.new(C.state)
        self.al = ALgoManage().set_state(self.s)
        return self

    def do_cmd(self, method, *args):
        try:
            if method == "put":
                pos = int(args[0]) * C.width + int(args[1])
                self.s = self.s.get_action(pos).get_dst()
            self.info(f"{method} {args}")
            self.info(self.s.show())
        except Exception as e:
            self.info(f"{method} {args} {e}")
            self.info(self.s.show())

    def view1(self):
        s = State.new(1100585500678)
        log.debug(s.show())
        for a in s.get_sort_actions():
            log.debug(a.show())
            log.debug(a.get_dst().show())

    def view2(self):
        s = State.new(1100585500678)
        log.debug(s.show())
        d = self.al.ab(5).search(s)
        log.debug(d.show())
        log.debug(d.dst.show())

    def view3(self):
        a = State.new(0x40200000000000000).get_action(25)

    def view4(self):
        from app.yly.envs.game.c5.gm_player import GmuMo

        s: State = State.new(2658648674848703515420644777517918216)
        # a = s.get_action(1 * C.width + 3)
        # s = a.get_dst()

        logger.debug(s.show())
        # al = GmuMo().load(C)
        # c = al.search(s, last_a=a)
        # logger.debug(c)

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
        from app.yly.envs.game.c5.gm_player import GmuMo

        logger.info(
            self.al.actor(
                [
                    GmuMo().load(C),
                    self.al.rd(),
                ]
            )[-1]
        )

    def fight(self):
        from app.yly.envs.game.c5.gm_player import GmuMo

        self.al.set_players([GmuMo(), self.al.rd()]).fight()

    def mc(self):
        s = State.new(CASE.get_case_6_61())
        log.debug(s.show())
        al = self.al.mc(1000)
        a = al.search(s)
        log.debug(a.show())
        log.debug(a.get_dst().show())
        log.debug(al.show())

    def mcactor(self):
        log.info(self.al.actor([self.al.mc()]))

    def ad(self):
        s = State.new(CASE.get_case_6_61())
        log.info(self.al.set_state(s).actor([self.al.ad(1)]))

    def dev(self):
        self.mc()

    def debug(self):
        self.view4()


if __name__ == "__main__":
    random_seed(4)
    C5Tool().run()
