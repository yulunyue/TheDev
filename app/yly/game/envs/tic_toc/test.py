from common.util.export import TestBase, logger, Module
from common.algo.export import ALgoManage, Algo, State, random_seed
from common.third_util.export import CodingGame
from .util import Pm
from .model.ttstate import TtState, TtAction
from .model.ttstate3 import TtState3
from .constant import C, SC
from .cg import TicTocCg


class TestTicToc(TestBase):
    def prepare(self, args=None):
        self.c = CodingGame(TicTocCg.name)

    def cg(self):
        Module().compile_one("app/yly/game/envs/tic_toc/cg.py")
        self.c.pk(Module.RUN_TMP_PATH, TicTocCg.game_id, TicTocCg.agentsIds)

    def replay(self):
        s = TtState.new_state(C.INIT_SATTE)
        for f in c.get_replay_json():
            action = C.op_pos(int(f.stdout[0]), int(f.stdout[2]))
            logger.info(s)
            a = s.get_action(action)
            s = a.dst
        TicTocCg().replay(c.get_replay_json())

    def actor(self):
        s = TtState.new_state(C.INIT_SATTE)
        ans = ALgoManage().set_state(s).actor([Pm.ab3, Pm.ab1], max_turn=101)
        logger.info(f"lose: {ans}")

    def search(self):
        s = TtState.new_state(C.INIT_SATTE).get_action(40).dst
        b: TtAction = Pm.ab2.search(s)
        logger.info(s)
        logger.info(b.dst)

    def fight(self):
        s = TtState.new_state(C.INIT_SATTE)
        ALgoManage().set_state(s).set_players([Pm.ab1, Pm.ab2, Pm.ab3, Pm.rd1]).fight()

    def dev3(self):
        s = TtState.new_state(98)
        logger.info(s)

    def test_dev4(self):
        self.run_ec_wrong(Pm.ab2)

    def run_ec_wrong(self, algo: Algo):
        for k, v in C.get_except_wrong().items():
            s = TtState.new_state(k)
            a = algo.search(s)
            self.expect(a.action not in v, True, f"{s}\n{a.action} not in {v}")

    def dev5(self):
        s = TtState.new_state(SC.SC1)
        Pm.bl1.search(s)
        logger.info(s.data["records"])

    def test_util(self):
        self.expect(C.op_pos(4, 4), 40)
        self.expect(C.pos_op(4), (3, 3))

    def test_tt3(self):
        t1 = TtState3.new(256)
        t2 = t1.get_action(1)
        self.expect(0, 1, f"{t1}\n{t2}")

    def run_t3(self):
        a = ALgoManage().set_record_dir(self.get_temp_path("t3"))
        a.set_state(TtState3.new())
        resutlt = a.actor([Pm.bl9, Pm.rd1])
        logger.info(resutlt)

    def debug(self):
        self.run_t3()


if __name__ == "__main__":
    random_seed(7)
    TestTicToc().run()
