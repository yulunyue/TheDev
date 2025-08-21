from common.util.export import logger
from app.yly.envs.cg.oa.model.state import Rooms
from common.mock import MockCg
from app.yly.envs.cg.oa.model.constant import C
from common.algo.search.alphabate_search import AlphaBateSearch, Algo


class PM:
    bl1 = AlphaBateSearch("bl1").load(1)
    bl2 = AlphaBateSearch("bl2").load(2)
    bl3 = AlphaBateSearch("bl3").load(3)
    bl4 = AlphaBateSearch("bl4").load(4)
    bl5 = AlphaBateSearch("bl5").load(5)
    ab3 = AlphaBateSearch("ab3").load(3, AlphaBateSearch.AB_TYPE)
    ab4 = AlphaBateSearch("ab4").load(4, AlphaBateSearch.AB_TYPE)
    ab5 = AlphaBateSearch("ab5").load(5, AlphaBateSearch.AB_TYPE)


class CgOa(MockCg):
    game_id = "7180187268449801570b2e5cd61f1efefe076e42"
    agentsIds = [-1, 5077834]
    name = "oa"
    uri = "https://www.codingame.com/ide/puzzle/oware-abapa"

    def get_action(self, s: Rooms, name="ab4"):
        if not name:
            actions = list(s.get_actions().values())
            return actions[0].action
        algo: Algo = getattr(PM, name)
        return algo.search(s).action

    def main(self):
        while True:
            s = Rooms.new(C.encode_data(0, self.ii()))
            a = self.get_action(s)
            self.log(state=s.state, action=a, board=s.boards)
            self.output(a)


if __name__ == "__main__":
    CgOa().main()
