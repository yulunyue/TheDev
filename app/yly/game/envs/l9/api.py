from common.service.export import Api
from common.util.export import logger
from app.yly.game.envs.l9.constant import C
from app.yly.game.envs.l9.model.l9state import L9State, L9Action, L9ENV


class L9Api(Api):
    def get_name(self):
        return "api"

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

    def search(self, s: L9State):
        data = self.get_moveinfo(
            L9ENV.dump_board(s.boards),
            s.player_id - 1,
            0 if s.depth < C.PLACES_MAX_TURN else 1,
        )
        error, moveInfos = data["error"], data["moveInfos"]
        if error:
            raise Exception(error,moveInfos)
        def util(a:L9Action):
            return [a.src_key,a.dst_key,a.remove_key]
        idx = min(range(len(moveInfos)),key=lambda v:moveInfos)
        actions = sorted(s.get_actions().values(),key=util)
        s.set_best_action(actions[idx])        
