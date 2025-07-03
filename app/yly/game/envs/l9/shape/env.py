from app.yly.game.envs.l9.constant import C
from app.yly.game.envs.l9.shape.chess import Chess
from app.yly.game.envs.l9.shape.line import Line
from typing import List, Dict


class L9Env:
    def load(self):
        self.INIT_STATE = "0" * (len(C.PLACES) + 1)
        self.chess_array = []
        self.chess_map = dict()
        self.chess_player_map: List[Dict[int, Chess]] = [dict(), dict(), dict()]
        for i, name in enumerate(C.PLACES):
            c = Chess(i, name)
            self.chess_map[c.name] = c
            self.chess_player_map[0][i] = c
            self.chess_array.append(c)
        self.lines: List[Line] = []
        for ln_str in C.LINES:
            ln = Line([self.chess_map[v] for v in ln_str.split(" ")])
            self.lines.append(ln)
        return self

    def dump(self):
        pass

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

    def load_from_board(self, boards):
        for i, v in enumerate(boards):
            self.chess_player_map[v][i] = self.chess_array[i]
        return self

    def get_actions(self, depth):
        if depth < C.PLACES_MAX_TURN:
            return self.get_place_actions(depth % 2 + 1)
        return self.get_move_actions(depth % 2 + 1)

    def get_place_actions(self, player_id):
        chesss: List[Chess] = self.chess_player_map[player_id].values()
        ret = []
        for c in chesss:
            can_remove = self.set_chess_player_id(c, player_id)
            if can_remove:
                for rc in self.get_can_removes_chess(2 - player_id):
                    ret.append([c.key, rc.key])
            else:
                ret.append([c.key, None])
            self.release_chess(c)

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

    def get_excepts(self):
        return {self.INIT_STATE: "PLACE A3"}


L9ENV = L9Env().load()
