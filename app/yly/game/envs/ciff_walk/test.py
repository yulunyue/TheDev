from common.util.export import TestBase, logger
from app.yly.game.envs.ciff_walk.env import CfState, ENV
from common.algo.export import (
    Sarsa,
    Qlearning,
    DynaQ,
    Algo,
    random_seed,
    MctsSearch,
    MctsEasy,
    np,
)


class CfTest(TestBase):

    def test_debug(self):
        self.test_algo(Qlearning().load())

    def test_base(self):
        self.test_algo(MctsEasy().load())
        self.test_algo(Qlearning().load())
        self.test_algo(DynaQ().load())
        self.test_algo(Sarsa().load())

    def test_algo(self, algo: Sarsa):
        for y, x, a in ENV.get_expects():
            state = CfState.new_one(y * ENV.ncol + x)
            self.expect(
                algo.search(state).action,
                a,
                f"algo:{algo.get_name()} y:{y},x:{x}\n {ENV.to_str()}",
            )
            key = f"{algo.get_name()}_{y}_{x}_{a}"
            logger.map(
                key=key,
                avg=np.mean(algo.rewards_record),
                var=np.var(algo.rewards_record),
            )
            logger.draw_line(key, algo.rewards_record)


if __name__ == "__main__":
    random_seed(0)
    CfTest().run()
