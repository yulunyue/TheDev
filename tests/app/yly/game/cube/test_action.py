import pytest
from common.util.export import TestBase
from app.yly.envs.game.cube.model import CubeState, CubeAction
from app.yly.envs.game.cube.constant import C


ACTION_TEST_CASES = [
    (0, 0, 1, ["  BB    ", "  BB    ", "YYOOWWRR", "OOWWRRYY", "  GG    ", "  GG    "]),
    (
        0,
        0,
        -1,
        ["  BB    ", "  BB    ", "WWRRYYOO", "OOWWRRYY", "  GG    ", "  GG    "],
    ),
    (0, 0, 2, ["  BB    ", "  BB    ", "RRYYOOWW", "OOWWRRYY", "  GG    ", "  GG    "]),
    (
        0,
        1,
        -1,
        ["  BB    ", "  BB    ", "OOWWRRYY", "WWRRYYOO", "  GG    ", "  GG    "],
    ),
    (0, 1, 1, ["  BB    ", "  BB    ", "OOWWRRYY", "YYOOWWRR", "  GG    ", "  GG    "]),
    (0, 1, 2, ["  BB    ", "  BB    ", "OOWWRRYY", "RRYYOOWW", "  GG    ", "  GG    "]),
    (1, 0, 1, ["  BW    ", "  BW    ", "OOWGRRBY", "OOWGRRBY", "  GY    ", "  GY    "]),
    (
        1,
        0,
        -1,
        ["  BY    ", "  BY    ", "OOWBRRGY", "OOWBRRGY", "  GW    ", "  GW    "],
    ),
    (1, 0, 2, ["  BG    ", "  BG    ", "OOWYRRWY", "OOWYRRWY", "  GB    ", "  GB    "]),
    (1, 1, 1, ["  WB    ", "  WB    ", "OOGWRRYB", "OOGWRRYB", "  YG    ", "  YG    "]),
    (
        1,
        1,
        -1,
        ["  YB    ", "  YB    ", "OOBWRRYG", "OOBWRRYG", "  WG    ", "  WG    "],
    ),
    (1, 1, 2, ["  GB    ", "  GB    ", "OOYWRRYW", "OOYWRRYW", "  BG    ", "  BG    "]),
    (2, 0, 1, ["  BB    ", "  OO    ", "OGWWBRYY", "OGWWBRYY", "  RR    ", "  GG    "]),
    (
        2,
        0,
        -1,
        ["  BB    ", "  RR    ", "OBWWGRYY", "OBWWGRYY", "  OO    ", "  GG    "],
    ),
    (2, 0, 2, ["  BB    ", "  GG    ", "ORWWORYY", "ORWWORYY", "  BB    ", "  GG    "]),
    (2, 1, 1, ["  RR    ", "  BB    ", "BOWWRGYY", "BOWWRGYY", "  GG    ", "  OO    "]),
    (
        2,
        1,
        -1,
        ["  OO    ", "  BB    ", "GOWWRBYY", "GOWWRBYY", "  GG    ", "  RR    "],
    ),
    (2, 1, 2, ["  GG    ", "  BB    ", "ROWWROYY", "ROWWROYY", "  GG    ", "  BB    "]),
]


class TestCubeAction(TestBase):
    @classmethod
    def setup_class(cls):
        CubeState.STATE_STORE = {}

    @pytest.mark.parametrize("axis,layer,rotate,expected", ACTION_TEST_CASES)
    def test_action_output(self, axis, layer, rotate, expected):
        s = CubeState.new_shape(C.SHAPE2)
        a = s.get_action((axis, layer, rotate))
        assert a.get_dst().to_str() == expected

    def test_action_show(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        msg = ""
        for action in actions:
            msg = action.show()
        self.expect("层" in msg, True)
        self.expect("轴" in msg, True)
        self.expect("旋转" in msg, True)

    def test_action_attributes(self):
        s = CubeState.new_shape(C.SHAPE2)
        for axis in range(C.AXIS_NUM):
            for layer in range(C.n):
                for rotate in C.MOVE_ACTION:
                    a = s.get_action((axis, layer, rotate))
                    self.expect(a.axis, axis)
                    self.expect(a.layer_id, layer)
                    self.expect(a.rotate, rotate)
                    self.expect(a.action, (axis, layer, rotate))

    def test_action_dst_immutable(self):
        s = CubeState.new_shape(C.SHAPE2)
        a = s.get_action((0, 0, 1))
        dst1 = a.get_dst()
        dst2 = a.get_dst()
        self.expect(dst1.state, dst2.state)

    def test_action_show_contains_rotation(self):
        s = CubeState.new_shape(C.SHAPE2)
        a = s.get_action((0, 0, 1))
        msg = a.show()
        self.expect("层" in msg, True)
        self.expect("轴" in msg, True)
        self.expect("旋转" in msg, True)
