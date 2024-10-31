from common.game.game_base import PlayerBase, Node, logger
inf = float("inf")


class AlphaBateSearch:

    def evaluate(self):
        return 0

    def get_moves(self, depth, last_move):
        return []

    def do(self, *mv):
        pass

    def undo(self, *mv):
        return

    def search(self, depth=10, last_move=None, alpha=-inf, bate=inf) -> None:
        if depth == 0:
            return None, self.evaluate(depth, last_move)
        mvs = self.get_moves(depth, last_move)
        if not mvs:
            return None, self.evaluate(depth, last_move)
        best_mv = mvs[0]
        for mv in mvs:
            self.do(mv)
            _, val = self.search(depth=depth-1, last_move=mv,
                                 alpha=-bate, bate=-alpha)
            val = -val
            self.undo(mv)
            if val >= bate:
                alpha = bate
                best_mv = mv
                break
            if val > alpha:
                alpha = val
                best_mv = mv
        return best_mv, alpha


class AlphaBateSearchDev(AlphaBateSearch, PlayerBase):

    def execute(self, i, env: Node):
        self.env = env
        best_mv, _ = self.search()
        return best_mv

    def evaluate(self, depth, mv: Node):
        logger.info(f'depth:{depth},mv:{mv.to_str()}')
        return mv.value

    def get_moves(self, depth, last_move: Node):
        if last_move is None:
            return self.env.childs
        return last_move.childs
