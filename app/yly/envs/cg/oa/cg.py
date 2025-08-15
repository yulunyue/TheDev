from common.util.export import logger
from app.yly.game.envs.oa.model.state import Rooms
from common.mock import MockCg
from app.yly.game.envs.oa.model.constant import C
from common.algo.search.alphabate_search import AlphaBateSearch, Algo


class PM:
    ab1 = AlphaBateSearch("ab1").load(1)
    ab2 = AlphaBateSearch("ab2").load(2)
    ab3 = AlphaBateSearch("ab3").load(3)
    ab4 = AlphaBateSearch("ab4").load(4)


class CgOa(MockCg):
    game_id = "7180187268449801570b2e5cd61f1efefe076e42"
    agentsIds = [-1, -2]
    name = "cgcw"

    def get_action(self, s: Rooms, name="ab2"):
        if not name:
            actions = list(s.get_actions().values())
            return actions[0].action
        algo: Algo = getattr(PM, name)
        return algo.search(s).action

    def main(self):
        while True:
            s = Rooms.new_room(0, self.ii())
            a = self.get_action(s)
            self.log(state=s.state, action=a, board=s.boards)
            self.output(a)


if __name__ == "__main__":
    CgOa().main()
