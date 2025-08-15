from common.util.export import TestBase, logger
from .env import CfState, C
from common.algo.export import (
    Td0,
    ValueIteration,
    PolicyIteration,
    Qlearning,
    DynaQ,
    Algo,
    random_seed,
    MctsSearch,
    MctsEasy,
    np,
)


class CfTest(TestBase):

    def test_value(self):
        self.run_algo(ValueIteration())

        # self.run_algo(MctsEasy().load())
        # self.run_algo(Qlearning().load())
        # self.run_algo(DynaQ().load())
        # self.run_algo(Td0().load())
        pass

    def run_algo(self, algo: Td0):
        for y, x, a in ENV.get_expects():
            state = CfState.new(y * ENV.ncol + x)
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
