from common.util.export import logger
from app.yly.envs.cg.oa.model.state import Rooms
from common.mock import MockCg
from app.yly.envs.cg.oa.model.constant import C
from common.algo.search.alphabate_search import AlphaBateSearch, Algo


class CgOa(MockCg):
    game_id = "7180187268449801570b2e5cd61f1efefe076e42"
    agentsIds = [5077834, -1]
    name = "oa"
    uri = "https://www.codingame.com/ide/puzzle/oware-abapa"

    def get_action(self, s: Rooms):
        al5 = AlphaBateSearch("ab5").load(5, AlphaBateSearch.AB_TYPE).set_params([1])
        return al5.search(s)

    def main(self):
        i = 0
        score = [0, 0]
        while True:
            boards = self.ii()
            if i == 0:
                if any([v != 4 for v in boards]):
                    i = 1
            all_score = sum(boards)
            s = Rooms.new(C.encode_data(0, i, score, boards))
            a = self.get_action(s)
            score[i % 2] = a.dst.score[i % 2]
            score[1 - i % 2] = 48 - all_score - score[i % 2]
            self.log(state=s.state, action=a.action, board=s.boards, score=score)
            self.output(a.action)
            i += 2


if __name__ == "__main__":
    CgOa().main()
