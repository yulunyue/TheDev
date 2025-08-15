from common.util.tool import auto, EnumAuto

CASES = [
    "....xx.xx....,....x...x....,.....x.x.....,.....x.x.....,..x.......x..,...x.....x...,..x.......x..|0 1 10 4 3 0,1 1 10 9 6 1,2 0 10 2 0 0,3 0 10 4 2 0,4 0 10 1 2 0,5 0 10 1 3 0,6 0 10 4 6 2,7 0 10 1 6 0,8 0 10 11 1 1,9 0 10 9 3 1,10 0 10 10 2 1,11 0 10 11 3 1,12 0 10 7 5 1,13 0 10 11 5 2",
    ".............,.x.x.....x.x.,.x.x.x.x.x.x.,.............,...x.....x...,.............,xx.........xx|0 1 10 4 3 0,1 1 10 10 2 1,2 0 10 2 2 0,3 0 10 1 5 0,4 0 10 4 2 0,5 0 10 1 3 0,6 0 10 3 0 2,7 0 10 5 1 2,8 0 10 10 0 1,9 0 10 11 5 1,10 0 10 8 0 2,11 0 10 10 4 1,12 0 10 9 0 2,13 0 10 7 0 2",
    ".............,.x.........x.,.x.........x.,.....x.x.....,.............,x...........x,.....x.x.....|0 1 6 3 0 0,2 0 10 2 4 0,3 0 10 3 5 0,4 0 10 4 5 0,5 0 4 3 2 0,7 0 10 4 2 0,8 0 10 12 6 1,11 0 1 9 3 1,12 0 2 9 0 1,13 0 10 10 1 1",
    "..x.x...x.x..,.............,.............,.............,x.x.......x.x,x...x...x...x,xx.........xx|0 1 10 4 3 0,1 1 10 10 3 1,2 0 10 4 2 0,3 0 10 3 0 2,4 0 10 3 2 0,5 0 10 5 5 2,6 0 10 5 4 2,7 0 10 2 1 2,8 0 10 8 2 2,9 0 10 9 1 2,10 0 10 9 2 1,11 0 10 7 5 2,12 0 10 7 2 2,13 0 10 9 3 1",
    "x....x.x....x,.............,.............,.............,.............,.............,x...x...x...x|0 1 4 2 2 0,2 0 10 4 0 0,4 0 10 2 5 0,5 0 10 1 1 0,6 0 10 2 0 0,7 0 10 4 5 2,8 0 10 9 2 1,9 0 10 8 1 1,10 0 10 10 5 1,11 0 10 9 3 1,12 0 10 10 1 1,13 0 10 6 6 2",
    "xx.x.x.x.x.xx,.............,....x...x....,.............,xx.........xx,.............,.............|0 1 10 4 5 0,1 1 10 9 4 1,2 0 10 1 6 2,3 0 10 4 3 0,4 0 10 5 3 2,5 0 10 2 1 0,6 0 10 1 1 0,7 0 10 5 5 2,8 0 10 11 6 2,9 0 10 6 4 1,10 0 10 6 1 2,11 0 10 9 1 2,12 0 10 11 1 1,13 0 10 9 5 1",
]


class Constant:
    obstacle = "obstacle"
    ACTION_WAIT = "WAIT"
    ACTION_MOVE = "MOVE"
    ACTION_SHOOT = "SHOOT"
    ACTION_CONVERT = "CONVERT"
    TYPE_OBS = "x"
    TYPE_NULL = "."
    VALUE_DAMAGE_MAX = 7
    UNITS_NUM = 14
    TYPE_CULTIST = 0
    OWNER_NEUTRAL = 2
    OWNER_PLAYER1 = 0
    OWNER_PLAYER2 = 1
    TYPE_CULT_LEADER = 1
    DR = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    WALL_S = "**"

    def get_cases(self):
        return {
            CASES[0]: [["0 MOVE 4 4"], ["0 MOVE 3 3"]],
            CASES[1]: [[], ["0 MOVE 4 4", "0 MOVE 5 3", "0 MOVE 3 3"]],
            CASES[2]: [[], ["0 MOVE 2 0"]],
            CASES[3]: [[], ["0 MOVE 4 4"]],
            CASES[4]: [[], ["0 MOVE 2 3"]],
            CASES[5]: [[], ["0 MOVE 4 6"]],
        }


class ValueEnum(EnumAuto):
    LEADER_IN_OP_CULT_RANGE = auto()
    WAIT_STATE = auto()
    NULL_STATE = auto()
    CULT_NEAR_OP_LEADER = auto()
    LEADER_AWAY_OP_CULT_RANGE = auto()
    LEADER_NEAR_NEUTRAL_CULT = auto()
    CULT_SHOOT_OP_CULT = auto()
    CULT_SHOOT_OP_LEADER = auto()
    LEADER_INFECT_NEUTRAL_CULT = auto()
    LEADER_OUT_OP_CULT_RANGE = auto()


VE = ValueEnum()
C = Constant()
