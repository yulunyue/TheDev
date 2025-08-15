from common.service.export import Api
from common.algo.export import Algo
from common.util.export import logger
from app.yly.game.envs.l9.constant import C
from app.yly.game.envs.l9.model.l9state import L9State, L9Action, L9ENV


class L9Api(Api):

    def get_endpoint(self):
        return C.PLAY_URI

    def get_moveinfo(self, board, player, placedPieces):
        return self.post_data(
            "/moveinfo",
            dict(
                board=str(board),
                player=player,
                placedPieces=placedPieces,
                timestamp=1751549085509,
                uuid="f152f7d0-e858-181b-fde4-51d683fb6674",
            ),
        )


class ApiAlgo(Algo):
    def get_max_actions(self, s: L9State):
        boards = L9ENV.dump_board(s.board)
        place_move = max(14 - s.place_move, 0)
        data = L9Api.ins().get_moveinfo(
            boards,
            s.player_id,
            place_move,
        )
        error, moveInfos = data["error"], data["moveInfos"]
        if len(moveInfos) == 0:
            return
        if error:
            raise Exception(error, moveInfos)

        def u(i, v):
            if v == 0:
                return [1, -v, i]
            if v % 2 == 0:
                return [0, v, i]
            return [2, -v, i]

        return sorted([u(i, v) for i, v in enumerate(moveInfos)])

    def search_main(self, s: L9State):
        def util(a: L9Action):
            return [a.src_key, a.dst_key, a.remove_key]

        actions = list(sorted(s.get_actions().values(), key=util))
        move_infos = self.get_max_actions(s)
        if len(move_infos) != len(actions):
            raise Exception(s, move_infos, actions)
        for i, a in enumerate(actions):
            a.set_data("score", move_infos[i])
        s.set_best_action(actions[move_infos[0][2]])
