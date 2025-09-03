from common.algo.search.param import Param, Params


class Constant:
    obstacle = "obstacle"
    ACTION_WAIT = "WAIT"
    ACTION_MOVE = "MOVE"
    ACTION_SHOOT = "SHOOT"
    ACTION_CONVERT = "CONVERT"
    TYPE_OBS = "x"
    TYPE_NULL = "."
    VALUE_DAMAGE_MAX = 7
    UNITS_CULTIST_NUM = 12
    OWNER_NEUTRAL = 2
    OWNER_PLAYER1 = 0
    OWNER_PLAYER2 = 1
    PLAYER_NUM = 2
    TYPE_CULTIST = 0
    TYPE_CULT_LEADER = 1
    DEFAULT_HP = 10
    DR = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    WALL_S = "**"


C = Constant()
