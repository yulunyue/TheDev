from common.util.export import ToolBase, logger, random
from common.algo.export import random_seed
from .model.mrp_state import MrpState, computer, C1
from .model.mdp_state import Mdp1State, Mdp2State, C2
from .value_func import Mcts


class Main(ToolBase):
    """
    https://hrl.boyuai.com/chapter/1/%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E5%86%B3%E7%AD%96%E8%BF%87%E7%A8%8B
    """

    def dev_mdp(self):
        s = MrpState.new(0)
        r = s.get_reward_by_actions([1, 2, 3, 6], gamma=0.5)
        logger.info(r)
        logger.info(computer(C1.MRP_REWARD, C1.MRP_P))

    def dev_mdp(self):
        mdp1 = Mdp1State.get_mrp_form_mdp()
        logger.info(computer(C2.MRP_REWARD, mdp1))
        logger.info(mdp1)

    def dev_mct(self):
        al = Mcts().load(0.5).set_train_epoll(1000)
        al.train(Mdp1State.new())
        logger.info(dict(al.vs))

    def dev(self):
        self.dev_mct()

    def debug(self):
        self.dev()


if __name__ == "__main__":
    random_seed(1)
    Main().run()
