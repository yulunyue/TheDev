from common.algo.export import Algo
from AlphaZero_Gomoku.mcts_alphaZero import MCTSPlayer
from AlphaZero_Gomoku.policy_value_net_pytorch import PolicyValueNet
from AlphaZero_Gomoku.policy_value_net_numpy import PolicyValueNetNumpy
from AlphaZero_Gomoku.game import Game, Board
from AlphaZero_Gomoku.train import TrainPipeline
from ..board.base import C, set_mask, BoardC5
from ..model.chess_static import ChessState, C5ACtion
from common.third_util.ml.np_util import np
from common.util.log import logger
import pickle


class C2(BoardC5):
    def set_state(self, state):
        super().set_state(state)
        self.b = Board(width=self.width, height=self.height, n_in_row=self.in_row)
        self.b.init_board()
        ct = [[], []]
        for i, v in enumerate(self.grid):
            if v:
                ct[v - 1].append(i)
        while ct[0]:
            self.b.do_move(ct[0].pop())
            if ct[1]:
                self.b.do_move(ct[1].pop())


class GmuMo(Algo):
    def load(self, c: BoardC5, model_path, use_pickle, n_playout=40):
        self.model_path = model_path
        if not use_pickle:
            p = PolicyValueNet(c.width, c.height, model_file=model_path)
            self.p = MCTSPlayer(p.policy_value_fn, n_playout=n_playout)
        else:
            policy_param = pickle.load(open(model_path, "rb"), encoding="bytes")
            best_policy = PolicyValueNetNumpy(c.width, c.height, policy_param)
            self.p = MCTSPlayer(
                best_policy.policy_value_fn, c_puct=5, n_playout=n_playout
            )
        self.c = C2().load(c.width, c.height, c.in_row)
        return super().load()

    def search_main(self, s: ChessState, last_a: C5ACtion = None):
        self.c.set_state(s.state)
        if last_a:
            self.c.b.last_move = last_a.action
        a = self.p.get_action(self.c.b).item()
        return s.get_action(a)

    def train(self, s):
        TrainPipeline(
            self.model_path,
            game_batch_num=1,
            batch_size=32,
            check_freq=1,
        ).run()
