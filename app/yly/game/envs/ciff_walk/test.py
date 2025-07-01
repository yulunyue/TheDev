from common.util.export import TestBase, logger
from app.yly.game.envs.ciff_walk.env import CfState, ENV
from common.algo.export import (
    Sarsa,
    Qlearning,
    DynaQ,
    Algo,
    random_seed,
    MctsSearchTree,
)


class Test(TestBase):
    def __init__(self):
        super().__init__()
        self.state = CfState.new_one()

    def test_dev(self):
        algo = DynaQ().load(n_planning=4)
        self.test_algo(algo)

    def test_base(self):
        self.test_algo(Qlearning().load())
        # self.test_algo(MctsSearchTree().load())

    def test_algo(self, algo: Sarsa):
        for s, a in ENV.get_expects():
            state = CfState.new_one(s)
            self.expect(algo.search(state).action, a, f"s:{s}\n {ENV.to_str()}")
            logger.draw_line(f"{algo.get_name()}_{s}_{a}", algo.rewards_record)
        logger.info(ENV.to_str())


if __name__ == "__main__":
    random_seed(0)
    Test().run()
