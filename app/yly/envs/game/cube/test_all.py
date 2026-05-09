from common.util.export import TestBase, log2 as logger, File
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
        a = s.get_action(0)
        assert a.get_dst().to_str() == [
            "  BB    ",
            "  BB    ",
            "OOWWRRYY",
            "YYOOWWRR",
            "  GG    ",
            "  GG    ",
        ]

    def test_all_actions_to_str(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        self.expect(len(actions), C.AXIS_NUM * C.n * len(C.MOVE_ACTION))
        expected = [
            # axis=0 (Blue/Green), layer=0
            ["  BB    ", "  BB    ", "OOWWRRYY", "YYOOWWRR", "  GG    ", "  GG    "],
            ["  BB    ", "  BB    ", "OOWWRRYY", "WWRRYYOO", "  GG    ", "  GG    "],
            ["  BB    ", "  BB    ", "OOWWRRYY", "RRYYOOWW", "  GG    ", "  GG    "],
            # axis=0, layer=1
            ["  BB    ", "  OO    ", "OOWWRRYY", "WWRRBBYY", "  GG    ", "  GG    "],
            ["  BB    ", "  RR    ", "OOWWRRYY", "BBOOWWYY", "  GG    ", "  GG    "],
            ["  BB    ", "  WW    ", "OOWWRRYY", "RRBBOOYY", "  GG    ", "  GG    "],
            # axis=1 (Orange/Red), layer=0
            ["  BY    ", "  BY    ", "OOGWRRWW", "OOGWRRYY", "  GG    ", "  BB    "],
            ["  BG    ", "  BG    ", "OOYWRRBB", "OOYWRRYY", "  GG    ", "  WW    "],
            ["  BW    ", "  BW    ", "OOBWRRGG", "OOBWRRYY", "  GG    ", "  YY    "],
            # axis=1, layer=1
            ["  GB    ", "  GB    ", "OOWYRRYY", "OOWYRRBB", "  WW    ", "  GG    "],
            ["  YB    ", "  YB    ", "OOWGRRYY", "OOWGRRWW", "  BB    ", "  GG    "],
            ["  WB    ", "  WB    ", "OOWBRRYY", "OOWBRRGG", "  YY    ", "  GG    "],
            # axis=2 (White/Yellow), layer=0
            ["  BB    ", "  BB    ", "OYWWGRRY", "OYWWGRRY", "  OG    ", "  OG    "],
            ["  BB    ", "  BB    ", "OGWWYROY", "OGWWYROY", "  RG    ", "  RG    "],
            ["  BB    ", "  BB    ", "ORWWORGY", "ORWWORGY", "  YG    ", "  YG    "],
            # axis=2, layer=1
            ["  RR    ", "  BB    ", "BBOOWWYY", "OOWWRRYY", "  GG    ", "  GG    "],
            ["  OO    ", "  BB    ", "WWRRBBYY", "OOWWRRYY", "  GG    ", "  GG    "],
            ["  WW    ", "  BB    ", "RRBBOOYY", "OOWWRRYY", "  GG    ", "  GG    "],
        ]
        for i, action in enumerate(actions):
            assert action.get_dst().to_str() == expected[i], (
                f"action {i} mismatch: {action.get_dst().to_str()} != {expected[i]}"
            )

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

    def test_actions_data_analysis(self):
        max_index = C.SIZE * C.n * C.n - 1
        logger.info(f"二阶魔方最大索引: {max_index}")

        for (axis, layer), action_groups in C.ACTIONS[C.SHAPE2].items():
            logger.info(f"\n分析动作 (axis={axis}, layer={layer}):")

            all_indices = set()
            for group_idx, group in enumerate(action_groups):
                logger.info(f"  组{group_idx}: {group}")

                for idx in group:
                    self.expect(0 <= idx <= max_index, True)
                    all_indices.add(idx)

                self.expect(len(group), 4)

            logger.info(f"  总共影响 {len(all_indices)} 个不同的小块")
            total_blocks = len(all_indices)
            logger.info(f"  唯一小块数: {total_blocks}")

        face_rotation = C.ACTIONS[C.SHAPE2][(0, 0)][0]
        self.expect(face_rotation, [0, 1, 3, 2])

        side_blocks = C.ACTIONS[C.SHAPE2][(0, 0)][1]
        logger.info(f"axis=0, layer=0 周边块: {side_blocks}")

        for face in range(6):
            face_indices = [face * 4 + i for i in range(4)]
            logger.info(f"面{face}索引: {face_indices}")

    def test_all_actions_coverage(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()

        expected_count = C.AXIS_NUM * C.n * len(C.MOVE_ACTION)
        self.expect(len(actions), expected_count)

        action_tuples = [a.action for a in actions]
        unique_actions = set(action_tuples)
        self.expect(len(unique_actions), expected_count)
