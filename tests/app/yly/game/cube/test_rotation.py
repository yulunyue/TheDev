from common.util.export import TestBase, log2 as logger
from app.yly.envs.game.cube.model import CubeState
from app.yly.envs.game.cube.constant import C


class TestRotation(TestBase):
    @classmethod
    def setup_class(cls):
        CubeState.STATE_STORE = {}
        cls.init_state = CubeState.new_shape(C.SHAPE2)

    def test_action_rotate_four_times_restore(self):
        s = CubeState.new_shape(C.SHAPE2)
        original_grid = s.grid.copy()
        original_state = s.state

        actions = s.make_actions()

        for i, action in enumerate(actions):
            axis = action.axis
            layer = action.layer_id
            rotate = action.rotate

            current = s
            rotate_times = 4 if rotate in [1, -1] else 2

            for step in range(rotate_times):
                current_actions = current.make_actions()
                target_action = None
                for a in current_actions:
                    if a.axis == axis and a.layer_id == layer and a.rotate == rotate:
                        target_action = a
                        break

                if not target_action:
                    logger.error(f"动作不存在: axis={axis}, layer={layer}, rotate={rotate}")
                    self.expect(False, True, f"动作不存在于步骤{step}")
                    continue

                current = target_action.get_dst()

            restored = current.grid == original_grid and current.state == original_state
            logger.info(
                f"动作{i}: axis={axis}, layer={layer}, rotate={rotate}, 旋转{rotate_times}次, 还原={restored}"
            )
            self.expect(
                restored,
                True,
                f"动作{i} (axis={axis}, layer={layer}, rotate={rotate}) 旋转{rotate_times}次未还原",
            )

    def test_rotate_4_same_action(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s.random_step(4)
        action_tuple = scrambled.get_sort_actions()[0].action
        state = scrambled
        for _ in range(4):
            a = state.get_action(action_tuple)
            state = a.get_dst()
        self.expect(state.state, scrambled.state)

    def test_rotate_4_layer1(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s.random_step(4)
        action_tuple = (1, 1, -1)
        state = scrambled
        for _ in range(4):
            a = state.get_action(action_tuple)
            state = a.get_dst()
        self.expect(state.state, scrambled.state)

    def test_rotate_cw_then_ccw(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s.random_step(4)
        cw = scrambled.get_action((0, 0, 1))
        ccw = cw.get_dst().get_action((0, 0, -1))
        self.expect(ccw.get_dst().state, scrambled.state)
