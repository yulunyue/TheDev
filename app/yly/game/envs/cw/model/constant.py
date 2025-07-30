from common.util.tool import auto, EnumAuto


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


class ValueEnum(EnumAuto):
    NULL_STATE = auto(0)
    LEADER_NEAR_NEUTRAL_CULT = auto()
    CULT_SHOOT_OP_CULT = auto()
    CULT_NEAR_OP_LEADER = auto()
    LEADER_INFECT_NEUTRAL_CULT = auto()
    CULT_SHOOT_OP_LEADER = auto()
    LEADER_AVOID_OP_CULT = auto()


VE = ValueEnum()
C = Constant()
