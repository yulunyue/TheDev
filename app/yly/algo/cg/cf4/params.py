from common.algo.search.param import Params, Param

INROW = 4


class ParamCt(Param):
    pass


class StateEnum(Params):
    def __init__(self):
        self.STATE_01 = ParamCt((1, 0)).load_value(1, 3)
        self.STATE_02 = ParamCt((2, 0)).load_value(1, 3)
        self.STATE_03 = ParamCt((3, 0)).load_value(10, 100)
        self.STATE_04 = ParamCt((4, 0)).load_value(200, 600)
        self.STATE_11 = ParamCt((1, 1)).load_value(800, 8000)
        self.STATE_12 = ParamCt((1, 2)).load_value(-100, -10)
        self.STATE_13 = ParamCt((1, 3)).load_value(-600, -200)

        super().__init__()


SE = StateEnum()
SE.init_param()
