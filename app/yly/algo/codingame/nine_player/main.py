from typing import List, Dict
import sys
PLACES = [
    "A1", "A4", "A7",
    "B2", "B4", "B6",
    "C3", "C4", "C5",
    "D1", "D2", "D3",
    "D5", "D6", "D7",
    "E3", "E4", "E5",
    "F2", "F4", "F6",
    "G1", "G4", "G7"
]

LINES = [
    'A1 A4 A7', 'A1 D1 G1', 'D1 D2 D3', 'D5 D6 D7',
    'A4 B4 C4', 'E4 F4 G4', 'A7 D7 G7', 'B2 B4 B6',
    'B2 D2 F2', 'B6 D6 F6', 'C3 C4 C5', 'C3 D3 E3',
    'C5 D5 E5', 'G1 G4 G7', 'F2 F4 F6', 'E3 E4 E5'
]


class Line:
    STATE_LINE_3 = ['111', '222']
    STATE_ALIVE_2 = [
        ['110', '101', '011'],
        ['220', '202', '022']
    ]

    def __init__(self, chesss) -> None:
        self.chesss: List[Chess] = chesss
        for i, c in enumerate(self.chesss):
            c.lines.append([i, self])
        self.chesss[0].next_chess.append(self.chesss[1])
        self.chesss[1].next_chess.append(self.chesss[0])
        self.chesss[1].next_chess.append(self.chesss[2])
        self.chesss[2].next_chess.append(self.chesss[1])

    def get_state(self):
        return "".join([str(v.player_id+1) for v in self.chesss])

    def info(self):
        return f'{"".join([v.key for v in self.chesss])}:{self.get_state()}'


class Chess:
    CHESS_NUMS = [0, 0]

    def __init__(self, index, key) -> None:
        self.key = key
        self.y = ord(key[0])-ord('A')
        self.x = int(key[1])-1
        self.index_score = index*0.01
        self.player_id = -1
        self.next_chess: List[Chess] = []
        self.lines = []
        self.actions: List[Action] = []
        self.dis_map = dict()
        BOARD_MAP[key] = self
        self.rest_step = 0

    def init(self):
        assert len(self.next_chess) >= 2 and len(self.next_chess) <= 4
        self.next_chess = sorted(
            self.next_chess, key=lambda v: PLACES.index(v.key))

    def draw_info(self):
        font_colcor = (255, 255, 255)
        if self.player_id == 0:
            font_colcor = (255, 128, 0)
        elif self.player_id == 1:
            font_colcor = (128, 255, 0)
        if self.rest_step:
            if self.player_id == -1:
                font_colcor = (0, 128, 255)
            return str(self.rest_step), font_colcor
        return self.key, font_colcor

    def set_player_id(self, player_id):
        if self.player_id != -1 and player_id == -1:
            Chess.CHESS_NUMS[self.player_id] -= 1
        elif self.player_id == -1 and player_id != -1:
            Chess.CHESS_NUMS[player_id] += 1
        self.player_id = player_id

    def is_in_line3(self, player_id):
        ln1: Line = self.lines[0][1]
        ln2: Line = self.lines[1][1]
        state_3 = Line.STATE_LINE_3[player_id]
        # print(ln1.info(), ln2.info(), state_3)
        if ln1.get_state() == state_3 or ln2.get_state() == state_3:
            return True
        return False


BOARD_MAP: Dict[str, Chess] = dict()


class Action:

    def __init__(self, method=None, key=None, next_key=None, remove_key=None) -> None:
        self.method = method
        self.key = key
        self.next_key = next_key
        self.remove_key = remove_key
        self.score = 0
        self.actions: List[Action] = []
        self.next_action: Action = None
        self.info = ""
        self.rest_step = 0

    def get_info(self):
        ret = []
        n: Action = self
        info = n.info
        while n:
            ret.append(str(n))
            info = n.info
            n = n.next_action
        return ";".join(ret), f'{info} {self.rest_step}'

    def place(self, key):
        self.method = 'PLACE'
        self.key = key
        return self

    def get_remove(self, keys):
        ret = []
        for key in keys:
            ret.append(Action(
                self.method+"&TAKE",
                self.key,
                self.next_key,
                key
            ))
        return ret

    def move(self, key1, key2):
        self.key = key1
        self.next_key = key2
        self.method = 'MOVE'
        return self

    def load(self, s: str):
        self.method, self.key, *args = s.split(";")
        if len(args) == 1:
            if self.method == 'PLACE&TAKE':
                self.remove_key = args[0]
            else:
                self.next_key = args[0]
        elif len(args) == 2:
            self.next_key, self.remove_key = args
        else:
            self.remove_key = None
        return self

    def __str__(self) -> str:
        ret = [self.method, self.key]
        if self.next_key:
            ret.append(self.next_key)
        if self.remove_key:
            ret.append(self.remove_key)
        return ';'.join(ret)


class Calc:
    k = [0, 0, -0.0651,  0.0692,  0.0292]

    def __init__(self, current_round, my_num, op_num, my_free, op_free, alive_2) -> None:
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
            ret += v*self.k[i]
        a.info = f'{ret}'
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
            self.lines.append(Line([BOARD_MAP[v]
                              for v in ln.split(' ')]))
        for m in self.boards:
            m.init()
        # self.init_chess_dis()
        self.player_id = player_id
        self.round = 0

    def get_board(self):
        return "".join([str(self.player_id)]+[str(v.player_id+1) for v in self.boards])

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
                        b.dis_map[c1.key] = n+1
                        # c1.dis_map[b.key] = n+1
                        stacks.append([c1, n+1])

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
        if a.method.startswith('PLACE'):
            BOARD_MAP[a.key].set_player_id(player_id)
        if a.method.startswith('MOVE'):
            tmp = BOARD_MAP[a.key].player_id
            BOARD_MAP[a.key].set_player_id(
                BOARD_MAP[a.next_key].player_id)
            BOARD_MAP[a.next_key].set_player_id(tmp)
        if a.method.endswith('TAKE'):
            BOARD_MAP[a.remove_key].set_player_id(remove_play_id)

        self.player_id = 1-self.player_id

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
            self.search(a, depth+1)
            if a.score > p.score:
                p.next_action = a
                p.score = a.score
            self.do_back_action(a)

    def get_line_state(self):
        alive_2 = 0
        for ln in self.lines:
            s = ln.get_state()
            if s in Line.STATE_ALIVE_2[1-self.player_id]:
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
        return [free_value[1-self.player_id], free_value[self.player_id]]

    def get_dis(self, c: Chess):
        ret = 0
        for c1 in self.boards:
            if c.key == c1.key:
                continue
            if c1.player_id == self.player_id:
                # print(c.key, c1.key, c.dis_map[c1.key])
                ret += abs(c.y-c1.y)+abs(c.x-c1.x)
        return [ret]

    def get_calc(self):
        args = self.get_free()+self.get_line_state()
        return Calc(self.round,
                    Chess.CHESS_NUMS[1-self.player_id],
                    Chess.CHESS_NUMS[self.player_id], *args)

    def get_actions(self) -> List[Action]:
        actions = []

        for c in self.boards:
            self.get_chess_action(c)
            actions.extend(c.actions)
        return actions

    def check_remove(self, a: Action):
        key = a.next_key if a .next_key else a.key
        # print(ln1.info(), ln2.info(), state_3)
        if BOARD_MAP[key].is_in_line3(self.player_id):
            return a.get_remove(self.get_remove())
        return [a]

    def get_remove(self):
        ret = []
        line_3_key = []
        for n in self.boards:
            if n.player_id != -1 and n.player_id != self.player_id:
                if n.is_in_line3(1-self.player_id):
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
            for v in c.next_chess if Chess.CHESS_NUMS[self.player_id] != 3 else self.boards:
                if v.player_id != -1:
                    continue
                a = Action().move(c.key, v.key)
                c.player_id, v.player_id = v.player_id, c.player_id
                c.actions.extend(self.check_remove(a))
                c.player_id, v.player_id = v.player_id, c.player_id

    def get_state(self):
        ret = 0 if self.is_place_state() else 1
        for c in self.boards:
            ret = ret*3+(c.player_id+1)
        return ret


if __name__ == "__main__":
    '''
    http://ninemensmorris.ist.tugraz.at:8080/ 
    '''
    player_id = int(input())  # playerId (0,1)
    ai = Ai(player_id)
    fields = int(input())  # number of fields
    for i in range(fields):
        neighbors = input()  # neighbors of a field (ex: A1:A4;D1)
    ai.init(neighbors)
    while True:
        # The last move executed from the opponent
        op_move = input()
        board = input()  # Current Board and state(0:Player0 | 1:Player1 | 2:Empty) in format field:state and separated by ;
        nbr = int(input())  # Number of valid moves proposed.
        if board == 1-player_id:
            ai.do_action(op_move)
        actions = []
        for i in range(nbr):
            actions.append(input())  # An executable command line
        # debug(f'actions:{actions}')
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        action = ai.get_best(actions)
        print(action)
        print(f"Debug messages...:{action}", file=sys.stderr, flush=True)
        ai.do_action(action)
