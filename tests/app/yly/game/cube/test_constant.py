from common.util.export import TestBase, log2 as logger
from app.yly.envs.game.cube.constant import C


class TestConstant(TestBase):
    @classmethod
    def setup_class(cls):
        C.load(C.SHAPE2)

    def test_constant(self):
        self.expect(C.SIZE, 6)
        self.expect(C.SHAPE2, 2)
        self.expect(C.AXIS_NUM, 3)
        self.expect(C.BIT_SIZE, 3)
        self.expect(len(C.COLORS), 6)
        self.expect(C.init_mask > 0, True)

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
