from app.yly.game.envs.l9.constant import C
from app.yly.game.envs.l9.shape.chess import Chess
from app.yly.game.envs.l9.shape.line import Line
from typing import List, Dict


def mask_down(mask, func):
    while mask:
        low_bit: int = mask & -mask
        i = low_bit.bit_length() - 1
        func(i)
        mask -= low_bit


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
        return self

    def dump(
        self,
        method,
        src_chess: Chess,
        remove_chess: Chess = None,
        dst_chess: Chess = None,
    ):
        return dict(
            method=method,
            src_key=src_chess.key,
            board=self.board,
            remove_key=remove_chess.key if remove_chess else None,
            dst_key=dst_chess.key if dst_chess else None,
        )

    def set_chess_player_id(self, c: Chess, player_id):
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

        c = self.chess_player_map[c.player_id].pop(c.key)
        self.chess_player_map[player_id][c.key] = c
        c.player_id = player_id
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
        self.reset()
        self.board = board

        def util(x):
            i, j = x // C.PLACE_NUM, x % C.PLACE_NUM
            self.set_chess_player_id(self.chess_map[C.PLACES[j]], i),

        mask_down(board, util)
        return self

    def get_actions(self, depth):
        if depth < C.PLACES_MAX_TURN:
            return self.get_place_actions(depth % 2 + 1)
        return self.get_move_actions(depth % 2 + 1)

    def get_place_actions(self, player_id):
        chesss: List[Chess] = list(self.chess_player_map[0].values())
        ret = []
        for c in chesss:
            can_remove = self.set_chess_player_id(c, player_id)
            if can_remove:
                for rc in self.get_can_removes_chess(2 - player_id):
                    ret.append(self.dump(C.PLACE, c, remove_chess=rc))
            else:
                ret.append(self.dump(C.PLACE, c))
            self.release_chess(c)
        return ret

    def get_can_removes_chess(self, player_id):
        chess: List[Chess] = self.chess_player_map[player_id].values()
        not_in_line3_chess = []
        for c in chess:
            if c.in_line:
                continue
            not_in_line3_chess.append(c)
        return not_in_line3_chess if not_in_line3_chess else chess

    def get_move_actions(self, player_id):
        pass

    def dump_board(self, mask):
        board = [0] * C.PLACE_NUM

        def util(x):
            i, j = x // C.PLACE_NUM, x % C.PLACE_NUM
            board[j] = i + 1

        mask_down(mask, util)
        return board

    def print_board(self, board):
        ret = [[" "] + [str(i + 1) for i in range(7)]]
        for i in range(7):
            ret.append([" "] * 8)
            ret[-1][0] = chr(ord("A") + i)
        for c in self.chess_map.values():
            y, x = c.get_pos()
            ret[y + 1][x + 1] = "O"

        def util(v):
            i, j = v // C.PLACE_NUM, v % C.PLACE_NUM
            y, x = self.chess_map[C.PLACE[j]].get_pos()
            ret[y + 1][x + 1] = "XY"[i]

        mask_down(board, util)
        return "\n" + "\n".join([" ".join(v) for v in ret]) + "\n"


L9ENV = L9Env().load()
