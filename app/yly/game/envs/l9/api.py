from common.service.export import Api
from common.algo.export import Algo
from common.util.export import logger
from app.yly.game.envs.l9.constant import C
from app.yly.game.envs.l9.model.l9state import L9State, L9Action, L9ENV


class L9Api(Api):
    def get_name(self):
        return "api"

    def get_endpoint(self):
        return C.PLAY_URI

    @classmethod
    def new(cls):
        return super().new().set_cache()

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
    def search_main(self, s: L9State):
        boards = L9ENV.dump_board(s.board)
        place_move = max(14 - s.place_move, 0)
        data = L9Api.new().get_moveinfo(
            boards,
            s.player_id,
            place_move,
        )
        error, moveInfos = data["error"], data["moveInfos"]
        if error:
            raise Exception(error, moveInfos)

        def util(a: L9Action):
            return [a.src_key, a.dst_key, a.remove_key]

        actions = sorted(s.get_actions().values(), key=util)
        if len(moveInfos) != len(actions):
            raise Exception(
                s, len(moveInfos), len(actions), actions, data, boards, place_move
            )
        idx = min(
            range(len(moveInfos)), key=lambda i: moveInfos[i] if moveInfos[i] else 10000
        )
        if idx < len(actions):
            s.set_best_action(actions[idx])
        else:
            raise Exception(s, actions, data, boards)
