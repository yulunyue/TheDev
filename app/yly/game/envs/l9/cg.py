from common.mock import CgMock
from common.algo.search.alphabate_search import AlphaBateSearch
from app.yly.game.envs.l9.model.l9state import L9State, L9Action


class Cgl9(CgMock):
    uri = ""
    game_id = ""
    agentsIds = [-1, 4820019]

    def get_ai(self):
        return AlphaBateSearch().load(max_depth=4, search_type=AlphaBateSearch.BR_TYPE)

    def run(self):
        player_id = int(self.input())  # playerId (0,1)
        ai = self.get_ai()
        fields = int(self.input())  # number of fields
        for i in range(fields):
            neighbors = self.input()  # neighbors of a field (ex: A1:A4;D1)
        st = L9State()
        while not st.done:
            # The last move executed from the opponent
            op_move, board, nbr = self.input(), self.input(), int(self.input())
            if board == 1 - player_id:
                st = st.get_action(op_move).dst
            actions = []
            for i in range(nbr):
                actions.append(st.get_action(self.input()))
            next_action: L9Action = ai.search(st)
            st = next_action.dst
            print(next_action.to_cg_str())
