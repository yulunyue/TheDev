from common.algo.export import Algo
from AlphaZero_Gomoku.mcts_alphaZero import MCTSPlayer
from AlphaZero_Gomoku.policy_value_net_pytorch import PolicyValueNet
from AlphaZero_Gomoku.policy_value_net_numpy import PolicyValueNetNumpy
from AlphaZero_Gomoku.game import Game, Board
from .constant import C, set_mask, ConstantC5
from .state import State, C5ACtion
from common.third_util.np_util import np
from common.util.log import logger
import pickle


class C2(ConstantC5):
    def set_state(self, state):
        super().set_state(state)
        self.b = Board(width=self.width, height=self.height, n_in_row=self.in_row)
        self.b.init_board()
        for i, v in enumerate(self.grid):
            if v:
                self.b.do_move(i)


BEST_MODEL_DIR = "D:/thebug/AlphaZero_Gomoku"


class GmuMo(Algo):
    def load(self, c: ConstantC5):

        if c.in_row == 4:
            p = PolicyValueNet(
                c.width, c.height, model_file=f"{BEST_MODEL_DIR}/best_policy.model"
            )
            self.p = MCTSPlayer(p)
        else:
            policy_param = pickle.load(
                open(f"{BEST_MODEL_DIR}/best_policy_8_8_5.model", "rb"),
                encoding="bytes",
            )
            best_policy = PolicyValueNetNumpy(c.width, c.height, policy_param)
            self.p = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)
        self.c = C2().load(c.width, c.height, c.in_row)
        return super().load()

    def search_main(self, s: State, last_a: C5ACtion):
        self.c.set_state(s.state)
        if last_a:
            self.c.b.last_move = last_a.action
        a = self.p.get_action(self.c.b).item()
        return s.get_action(a)
