from common.util.export import logger
from app.yly.envs.cg.oa.model.state import Rooms
from common.mock import MockCg
from app.yly.envs.cg.oa.model.constant import C
from common.algo.search.alphabate_search import AlphaBateSearch, Algo


class CgOa(MockCg):
    game_id = "7180187268449801570b2e5cd61f1efefe076e42"
    agentsIds = [-1, 5077834]
    name = "oa"
    uri = "https://www.codingame.com/ide/puzzle/oware-abapa"

    def get_action(self, s: Rooms):
        al5 = AlphaBateSearch("ab5").load(5, AlphaBateSearch.AB_TYPE)
        return al5.search(s).action

    def main(self):
        while True:
            s = Rooms.new(C.encode_data(0, self.ii()))
            a = self.get_action(s)
            self.log(state=s.state, action=a, board=s.boards)
            self.output(a)


if __name__ == "__main__":
    CgOa().main()
