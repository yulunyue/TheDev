from common.algo.search.param import Param, Params


class CASES:
    MAP1 = """....xx.xx....,....x...x....,.....x.x.....,.....x.x.....,..x.......x..,...x.....x...,..x.......x.."""
    S1_1 = "0 1 10 4 3 0,1 1 10 9 6 1,2 0 10 2 0 0,3 0 10 4 2 0,4 0 10 1 2 0,5 0 10 1 3 0,6 0 10 4 6 2,7 0 10 1 6 0,8 0 10 11 1 1,9 0 10 9 3 1,10 0 10 10 2 1,11 0 10 11 3 1,12 0 10 7 5 1,13 0 10 11 5 2"
    cases = {
        MAP1: {
            S1_1: "",
        }
    }


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
    DATA_POS_unit_id = 0
    DATA_POS_unit_type = 1
    DATA_POS_hp = 2
    DATA_POS_x = 3
    DATA_POS_y = 4
    DATA_POS_owner = 5


C = Constant()
