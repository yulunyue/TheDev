from .base_state import BoardC5State


class BoardMove(BoardC5State):

    def change_chess_statu(self, idx, player_id):
        super().change_chess_statu(idx, player_id)
