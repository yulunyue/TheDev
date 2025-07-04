from app.yly.game.envs.l9.constant import C
from app.yly.game.envs.l9.shape.chess import Chess
from app.yly.game.envs.l9.shape.line import Line
from typing import List, Dict
from common.util.export import logger


def mask_down(mask, func):
    i = 0
    while mask:
        func(i, mask & 3)
        i += 1
        mask = mask >> 2


class L9Env:

    def load(self):
        self.INIT_STATE = 0
        self.chess_map: Dict[str, Chess] = dict()
        for i, key in enumerate(C.PLACES):
            c = Chess(key, i)
            self.chess_map[c.key] = c
        self.lines: List[Line] = []
        for ln_str in C.LINES:
            ln = Line([self.chess_map[v] for v in ln_str.split(" ")])
            self.lines.append(ln)
        self.reset()
        return self

    def dump(
        self,
        method,
        src_chess: Chess,
        dst_chess: Chess,
        remove_chess: Chess,
        place_move,
        player_id: int,
    ):
        return dict(
            method=method,
            src_key=src_chess.key,
            board=self.board,
            done=place_move == 0
            and len(list(self.chess_player_map[player_id].values())) <= 2,
            remove_key=remove_chess.key if remove_chess else None,
            dst_key=dst_chess.key if dst_chess else None,
        )

    def update_chess(self, c: Chess, player_id):
        can_remove = False
        if player_id == 0:
            add_num = -1 if c.player_id == 2 else 1
        else:
            add_num = -1 if player_id == 1 else 1
        for ln in c.lines:
            last_chess_num, new_chess_num = ln.chess_num, ln.chess_num + add_num
            sm = last_chess_num + new_chess_num
            if sm == 5 or sm == -5:
                can_remove = True
                for c2 in ln.chess_array:
                    c2.in_line += 1 if new_chess_num == -2 or new_chess_num == 3 else -1
            ln.chess_num = new_chess_num
        return can_remove

    def set_chess_player_id(self, c: Chess, player_id):
        if c.player_id == player_id:
            return False
        can_remove = self.update_chess(c, player_id)
        c = self.chess_player_map[c.player_id].pop(c.key)
        self.chess_player_map[player_id][c.key] = c
        board = c.set_player_id(self.board, player_id)
        # logger.info(f"--{c.key}-{c.idx}-{player_id}--\n{bin(self.board)}\n{bin(board)}")
        self.board = board
        return can_remove

    def release_chess(self, c: Chess):
        return self.set_chess_player_id(c, 0)

    def reset(self):
        self.chess_player_map: List[Dict[int, Chess]] = [
            self.chess_map.copy(),
            dict(),
            dict(),
        ]
        for ln in self.lines:
            ln.reset()
        for c in self.chess_map.values():
            c.reset()

    def load_from_board(self, board):
        self.board = board

        def util(i, x):
            self.set_chess_player_id(self.chess_map[C.PLACES[i]], x),

        mask_down(board, util)
        return self

    def get_actions(self, player_id, place_move):
        if place_move:
            return self.get_place_actions(player_id, place_move)
        return self.get_move_actions(player_id, place_move)

    def add_actions(
        self, player_id, can_remove, src: Chess, dst: Chess, method, place_move
    ):
        ret = []
        if can_remove:
            for rc in self.get_can_removes_chess(3 - player_id):
                self.release_chess(rc)
                ret.append(
                    self.dump(method + "&TAKE", src, dst, rc, place_move, player_id)
                )
                self.set_chess_player_id(rc, 3 - player_id)
        else:
            ret.append(self.dump(method, src, dst, None, place_move, player_id))
        return ret

    def get_place_actions(self, player_id, place_move):
        chesss: List[Chess] = list(self.chess_player_map[0].values())
        ret = []
        for c in chesss:
            can_remove = self.set_chess_player_id(c, player_id)
            ret.extend(
                self.add_actions(
                    player_id, can_remove, c, None, C.PLACE_ACTION, place_move
                )
            )
            self.release_chess(c)
        return ret

    def get_can_removes_chess(self, player_id: int):
        chess: List[Chess] = list(self.chess_player_map[player_id].values())
        not_in_line3_chess = []
        for c in chess:
            if c.in_line:
                continue
            not_in_line3_chess.append(c)
        return not_in_line3_chess if not_in_line3_chess else chess

    def move(self, player_id, c1: Chess, c2: Chess):
        self.release_chess(c1)
        return self.set_chess_player_id(c2, player_id)

    def get_move_actions(self, player_id: int, place_move):
        chesss: List[Chess] = list(self.chess_player_map[player_id].values())
        ret = []
        can_null_moves = []
        if len(chesss) <= 3:
            can_null_moves = list(self.chess_player_map[0].values())

        for c in chesss:
            can_moves = c.nexts
            if can_null_moves:
                can_moves = can_null_moves
            for nc in can_moves:
                if nc.player_id:
                    continue
                can_remove = self.move(player_id, c, nc)
                ret.extend(
                    self.add_actions(
                        player_id, can_remove, c, nc, C.MOVE_ACTION, place_move
                    )
                )
                self.move(player_id, nc, c)
        return ret

    def dump_board(self, mask):
        board = [0] * C.PLACE_NUM

        def util(i, x):
            board[i] = x

        mask_down(mask, util)
        return board

    def print_board(self, board):
        ret = []
        for i in range(7, 0, -1):
            ret.append([" "] * 8)
            ret[-1][0] = str(i)

        for c in self.chess_map.values():
            y, x = c.get_pos()
            ret[y][x + 1] = " "

        def util(i, v):
            y, x = self.chess_map[C.PLACES[i]].get_pos()
            ret[6 - y][x + 1] = " *#"[v]

        mask_down(board, util)
        ret.append([" "] + [chr(ord("A") + i) for i in range(7)])
        return "\n" + "\n".join([" ".join(v) for v in ret]) + "\n"


L9ENV = L9Env().load()
