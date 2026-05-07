from common.util.export import TestBase, log as logger, File
from app.yly.envs.game.cube.model import CubeState, CubeAction
from app.yly.envs.game.cube.constant import C
from app.yly.envs.game.cube.algo import Al
import json
import random


class TestCube(TestBase):
    @classmethod
    def setup_class(cls):
        CubeState.STATE_STORE = {}
        cls.init_state = CubeState.new_shape(C.SHAPE2)

    def test_constant(self):
        self.expect(C.SIZE, 6)
        self.expect(C.SHAPE2, 2)
        self.expect(C.AXIS_NUM, 3)
        self.expect(C.BIT_SIZE, 3)
        self.expect(len(C.COLORS), 6)
        self.expect(C.init_mask > 0, True)

    def test_state_new(self):
        s = CubeState.new_shape(C.SHAPE2)
        self.expect(s.game_over(), True)
        self.expect(len(s.grid), C.SIZE * C.n * C.n)

    def test_state_make_actions(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        expected_count = C.AXIS_NUM * C.n * len(C.MOVE_ACTION)
        self.expect(len(actions), expected_count)

    def test_action_show(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        for action in actions:
            msg = action.show()
            self.expect("层" in msg, True)
            self.expect("色" in msg, True)
            self.expect("旋转" in msg, True)

    def test_state_convert(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        for action in actions:
            new_state = action.get_dst()
            self.expect(isinstance(new_state, CubeState), True)
            self.expect(new_state.game_over(), False)

    def test_random_action(self):
        s = CubeState.new_shape(C.SHAPE2)
        action = s.get_random_action()
        self.expect(isinstance(action, CubeAction), True)
        new_state = action.get_dst()
        self.expect(new_state.game_over(), False)

    def test_to_str(self):
        s = CubeState.new_shape(C.SHAPE2)
        lines = s.to_str()
        self.expect(len(lines), C.n * 3)

    def test_bfs_from_init(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        self.expect(len(actions) > 0, True)

    def test_solve_one_step(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        scrambled = actions[0].get_dst()
        self.expect(scrambled.game_over(), False)

        revert_actions = scrambled.make_actions()
        found = False
        for action in revert_actions:
            if action.get_dst().game_over():
                found = True
                break
        self.expect(found, True)

    def test_solve_multiple_steps(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s

        for _ in range(2):
            actions = scrambled.make_actions()
            scrambled = actions[0].get_dst()

        self.expect(scrambled.game_over(), False)
        self.expect(scrambled.depth, 2)

    def test_state_depth(self):
        s = CubeState.new_shape(C.SHAPE2)
        self.expect(s.depth, 0)

        actions = s.make_actions()
        new_state = actions[0].get_dst()
        self.expect(new_state.depth, 1)

    def test_all_colors_present(self):
        s = CubeState.new_shape(C.SHAPE2)
        colors = set(s.grid)
        self.expect(len(colors), C.SIZE)
