from common.util.export import TestBase, logger, Module
from common.algo.export import (
    ALgoManage,
    FIGHT_TYPE,
    Algo,
    State,
    Td0,
    random_seed,
    MctsSearch,
    AbDev,
    RandomAlgo,
)
from common.third_service.export import CodingGame, uu
from .model.ttstate import TtState, TtAction
from .model.ttstate3 import TtState3
from .constant import C
from .cg import TicTocCg


class TestTicToc(TestBase):
    def prepare(self, args=None):
        self.c = CodingGame(TicTocCg.name)
        self.s3 = TtState3.new(C.INIT_STATE)
        self.s9 = TtState.new(C.INIT_STATE81)
        self.td0 = Td0("td0").load()
        self.mc = MctsSearch("mc").load(num_episodes=50)
        self.al3 = ALgoManage().set_state(self.s3).set_record_dir(uu(TicTocCg.name))

    def run_s9(self):
        logger.info(self.s9)

    def cg_play(self):
        Module().compile_one(TicTocCg.main_py())
        self.c.pk(Module.RUN_TMP_PATH, TicTocCg.game_id, TicTocCg.agentsIds)

    def dev(self):
        self.td0.search(self.s3)

    def run_mcts(self):
        self.mc.search(self.s3)

    def run_ec_wrong(self, algo: Algo):
        for k, v in C.get_except_wrong().items():
            s = TtState.new_state(k)
            a = algo.search(s)
            self.expect(a.action not in v, True, f"{s}\n{a.action} not in {v}")

    def test_al3(self):
        self.al3.set_players(
            [
                ab(10),
                # self.mc,
                self.td0,
            ]
        ).fight(tp=FIGHT_TYPE.DTURN, pk_round=20)
        # self.expect(self.al3.a_r[self.mc.name].LOSE,0,self.al3)
        logger.info(self.al3)
        self.expect(self.al3.a_r[self.td0.name].LOSE, 0, self.al3)

    def test_util(self):
        self.expect(C.op_pos(4, 4), 40)
        self.expect(C.pos_op(4), (3, 3))

    def run_t32(self):
        pass

    def debug(self):
        self.run_mcts()


if __name__ == "__main__":
    random_seed(7)
    TestTicToc().run()
