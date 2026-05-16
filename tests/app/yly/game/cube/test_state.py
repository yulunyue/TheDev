from common.algo.export import decode_data
from common.util.export import TestBase
from app.yly.envs.game.cube.model import CubeState, CubeAction
from app.yly.envs.game.cube.constant import C


class TestCubeState(TestBase):
    @classmethod
    def setup_class(cls):
        CubeState.STATE_STORE = {}
        cls.init_state = CubeState.new_shape(C.SHAPE2)

    def test_state_new(self):
        s = CubeState.new_shape(C.SHAPE2)
        self.expect(s.game_over(), True)
        self.expect(len(s.grid), C.SIZE * C.n * C.n)

    def test_state_make_actions(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        expected_count = C.AXIS_NUM * C.n * len(C.MOVE_ACTION)
        self.expect(len(actions), expected_count)

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
        a = s.get_action((0, 0, -1))
        assert a.get_dst().to_str() == [
            "  BB    ",
            "  BB    ",
            "WWRRYYOO",
            "OOWWRRYY",
            "  GG    ",
            "  GG    ",
        ]

    def test_to_str2(self):
        s = CubeState.new_shape(C.SHAPE2)
        assert s.to_str() == [
            "  BB    ",
            "  BB    ",
            "OOWWRRYY",
            "OOWWRRYY",
            "  GG    ",
            "  GG    ",
        ]
        a = s.get_action((1, 0, 2))
        assert a.get_dst().to_str() == [
            "  BG    ",
            "  BG    ",
            "OOWYRRWY",
            "OOWYRRWY",
            "  GB    ",
            "  GB    ",
        ]

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

    def test_serialization_roundtrip(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s.random_step(5)
        data = scrambled.to_json()
        self.expect("state" in data, True)
        self.expect("depth" in data, True)
        self.expect("n" in data, True)
        self.expect("game_over" in data, True)

        restored = CubeState(0).load_from_json(data)
        self.expect(restored.state, scrambled.state)
        self.expect(restored.depth, scrambled.depth)
        self.expect(restored.game_over(), scrambled.game_over())

    def test_get_action_tuple_lookup(self):
        s = CubeState.new_shape(C.SHAPE2)
        for axis in range(C.AXIS_NUM):
            for layer in range(C.n):
                for rotate in C.MOVE_ACTION:
                    a = s.get_action((axis, layer, rotate))
                    self.expect(isinstance(a, CubeAction), True)
                    self.expect(a.action, (axis, layer, rotate))

    def test_get_action_invalid_raises(self):
        s = CubeState.new_shape(C.SHAPE2)

        def try_get(v):
            try:
                s.get_action(v)
                return None
            except Exception as e:
                return str(e)

        self.expect(try_get((99, 0, 1)) is not None, True)
        self.expect(try_get((0, 99, 1)) is not None, True)
        self.expect(try_get((0, 0, 99)) is not None, True)

    def test_make_actions_from_scrambled(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s.random_step(5)
        actions = scrambled.make_actions()
        expected_count = C.AXIS_NUM * C.n * len(C.MOVE_ACTION)
        self.expect(len(actions), expected_count)
        for a in actions:
            self.expect(a.src.state, scrambled.state)
            ns = a.get_dst()
            self.expect(not ns.game_over(), True)

    def test_grid_consistency(self):
        s = CubeState.new_shape(C.SHAPE2)
        for _ in range(10):
            a = s.get_random_action()
            s = a.get_dst()
            decoded = decode_data(s.state, [C.BIT_SIZE] * (C.SIZE * C.n * C.n))
            self.expect(decoded, s.grid)

    def test_random_step(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s.get_sort_actions()[0].get_dst()
        self.expect(not scrambled.game_over(), True)
        result = scrambled.random_step(7)
        self.expect(isinstance(result, CubeState), True)
        self.expect(result.depth >= scrambled.depth + 1, True)

    def test_all_actions_coverage(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()

        expected_count = C.AXIS_NUM * C.n * len(C.MOVE_ACTION)
        self.expect(len(actions), expected_count)

        action_tuples = [a.action for a in actions]
        unique_actions = set(action_tuples)
        self.expect(len(unique_actions), expected_count)
