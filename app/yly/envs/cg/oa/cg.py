from common.util.export import logger
from app.yly.envs.cg.oa.model.state import StateBase
from common.mock import MockCg
from app.yly.envs.cg.oa.model.constant import C
from common.algo.search.alphabate_search import AlphaBateSearch, Algo


class CgOa(MockCg):
    game_id = "7180187268449801570b2e5cd61f1efefe076e42"
    agentsIds = [-1, 5077834]
    name = "oa"
    uri = "https://www.codingame.com/ide/puzzle/oware-abapa"

    def get_action(self, s: StateBase):
        al5 = AlphaBateSearch().load(5, AlphaBateSearch.AB_TYPE)
        return al5.search(s)

    def main(self):
        reward = 0
        i = 0
        while True:
            boards = self.ii()
            if i == 0 and any([v != 4 for v in boards]):
                i = 1
            s = StateBase.new(C.encode_data(i, reward, boards))
            a = self.get_action(s)
            reward += a.get_reward()
            i += 2
            self.log(state=s.state, board=boards, reawd=reward)
            self.output(a.action)


if __name__ == "__main__":
    CgOa().main()
