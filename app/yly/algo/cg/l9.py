from typing import List, Dict
import sys


BOARD_MAP: Dict[str, Chess] = dict()


class Calc:
    k = [0, 0, -0.0651, 0.0692, 0.0292]

    def __init__(
        self, current_round, my_num, op_num, my_free, op_free, alive_2
    ) -> None:
        self.current_round = current_round
        self.my_num = my_num
        self.op_num = op_num
        self.my_free = my_free
        self.op_free = op_free
        self.alive_2 = alive_2
        self.exp_value = 0

    def x(self):
        return [self.my_num, self.op_num, self.my_free, self.op_free, self.alive_2]

    def execute(self, a: Action):
        ret = 0
        for i, v in enumerate(self.x()):
            ret += v * self.k[i]
        a.info = f"{ret}"
        return ret


class Ai:
    TMOUT = 50
    MAX_DEPTH = 1
    MAX_VALUE = 100
    MIN_VALUE = -100

    def __init__(self, player_id) -> None:
        self.actions: List[Action] = []
        self.boards: List[Chess] = []
        self.lines: List[Line] = []
        for i, m in enumerate(PLACES):
            self.boards.append(Chess(i, m))
        for ln in LINES:
            self.lines.append(Line([BOARD_MAP[v] for v in ln.split(" ")]))
        for m in self.boards:
            m.init()
        # self.init_chess_dis()
        self.player_id = player_id
        self.round = 0

    def get_board(self):
        return "".join(
            [str(self.player_id)] + [str(v.player_id + 1) for v in self.boards]
        )

    def init_chess_dis(self):
        for b in self.boards:
            stacks = [[b, 0]]

            while len(stacks):
                _, n = stacks.pop(0)
                c: Chess = _
                for c1 in c.next_chess:
                    if c1.key == b.key:
                        continue
                    if c1.key not in b.dis_map:
                        b.dis_map[c1.key] = n + 1
                        # c1.dis_map[b.key] = n+1
                        stacks.append([c1, n + 1])

    def is_place_state(self):
        return self.round < 18

    def do_action(self, a):
        self.actions.append(a)
        self.execute_action(a, self.player_id, -1)
        self.round += 1
        return a

    def do_action_str(self, a):
        return self.do_action(Action().load(a))

    def do_back_action(self, action):
        self.execute_action(action, -1, self.player_id)
        self.round -= 1
        self.actions.pop()

    def execute_action(self, a: Action, player_id, remove_play_id):
        if a.method.startswith("PLACE"):
            BOARD_MAP[a.key].set_player_id(player_id)
        if a.method.startswith("MOVE"):
            tmp = BOARD_MAP[a.key].player_id
            BOARD_MAP[a.key].set_player_id(BOARD_MAP[a.next_key].player_id)
            BOARD_MAP[a.next_key].set_player_id(tmp)
        if a.method.endswith("TAKE"):
            BOARD_MAP[a.remove_key].set_player_id(remove_play_id)

        self.player_id = 1 - self.player_id

    def get_best(self, *args) -> Action:
        root_action = Action()
        self.search(root_action)
        return root_action

    def search(self, p: Action, depth=0):
        if depth >= self.MAX_DEPTH:
            p.score = self.get_calc().execute(p)
            return
        p.actions = self.get_actions()
        p.score = self.MIN_VALUE
        for a in p.actions:
            self.do_action(a)
            self.search(a, depth + 1)
            if a.score > p.score:
                p.next_action = a
                p.score = a.score
            self.do_back_action(a)

    def get_line_state(self):
        alive_2 = 0
        for ln in self.lines:
            s = ln.get_state()
            if s in Line.STATE_ALIVE_2[1 - self.player_id]:
                alive_2 += 1
        return [alive_2]

    def get_free(self):
        free_value = [0, 0]

        for c in self.boards:

            if c.player_id == -1:
                continue
            for c1 in c.next_chess:
                if c1.player_id == -1:
                    free_value[c.player_id] += 1
        return [free_value[1 - self.player_id], free_value[self.player_id]]

    def get_dis(self, c: Chess):
        ret = 0
        for c1 in self.boards:
            if c.key == c1.key:
                continue
            if c1.player_id == self.player_id:
                # print(c.key, c1.key, c.dis_map[c1.key])
                ret += abs(c.y - c1.y) + abs(c.x - c1.x)
        return [ret]

    def get_calc(self):
        args = self.get_free() + self.get_line_state()
        return Calc(
            self.round,
            Chess.CHESS_NUMS[1 - self.player_id],
            Chess.CHESS_NUMS[self.player_id],
            *args,
        )

    def get_actions(self) -> List[Action]:
        actions = []

        for c in self.boards:
            self.get_chess_action(c)
            actions.extend(c.actions)
        return actions

    def check_remove(self, a: Action):
        key = a.next_key if a.next_key else a.key
        # print(ln1.info(), ln2.info(), state_3)
        if BOARD_MAP[key].is_in_line3(self.player_id):
            return a.get_remove(self.get_remove())
        return [a]

    def get_remove(self):
        ret = []
        line_3_key = []
        for n in self.boards:
            if n.player_id != -1 and n.player_id != self.player_id:
                if n.is_in_line3(1 - self.player_id):
                    line_3_key.append(n.key)
                else:
                    ret.append(n.key)
        return ret if len(ret) else line_3_key

    def get_chess_action(self, c: Chess):
        c.actions = []
        if self.is_place_state():
            if c.player_id == -1:
                a = Action().place(c.key)
                c.player_id = self.player_id
                c.actions.extend(self.check_remove(a))
                c.player_id = -1
        else:
            if c.player_id != self.player_id:
                return
            for v in (
                c.next_chess if Chess.CHESS_NUMS[self.player_id] != 3 else self.boards
            ):
                if v.player_id != -1:
                    continue
                a = Action().move(c.key, v.key)
                c.player_id, v.player_id = v.player_id, c.player_id
                c.actions.extend(self.check_remove(a))
                c.player_id, v.player_id = v.player_id, c.player_id

    def get_state(self):
        ret = 0 if self.is_place_state() else 1
        for c in self.boards:
            ret = ret * 3 + (c.player_id + 1)
        return ret
