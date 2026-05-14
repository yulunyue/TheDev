from common.algo.export import decode_data
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
        self.expect("轴" in msg, True)
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
        a = s.get_action((1, 0, 2))  # axis=1 (x轴), layer=0, rotate=180°
        assert a.get_dst().to_str() == [
            "  BG    ",
            "  BG    ",
            "OOWYRRWY",
            "OOWYRRWY",
            "  GB    ",
            "  GB    ",
        ]

    def test_all_actions_to_str(self):
        s = CubeState.new_shape(C.SHAPE2)
        actions = s.make_actions()
        self.expect(len(actions), C.AXIS_NUM * C.n * len(C.MOVE_ACTION))
        expected = [
            # action 0: axis=0 (y轴), layer=0, rotate=-1
            [
                "  BB    ",
                "  BB    ",
                "WWRRYYOO",
                "OOWWRRYY",
                "  GG    ",
                "  GG    ",
            ],
            # action 1: axis=0, layer=0, rotate=1
            [
                "  BB    ",
                "  BB    ",
                "YYOOWWRR",
                "OOWWRRYY",
                "  GG    ",
                "  GG    ",
            ],
            # action 2: axis=0, layer=0, rotate=2
            [
                "  BB    ",
                "  BB    ",
                "RRYYOOWW",
                "OOWWRRYY",
                "  GG    ",
                "  GG    ",
            ],
            # action 3: axis=0, layer=1, rotate=-1
            [
                "  BB    ",
                "  BB    ",
                "OOWWRRYY",
                "WWRRYYOO",
                "  GG    ",
                "  GG    ",
            ],
            # action 4: axis=0, layer=1, rotate=1
            [
                "  BB    ",
                "  BB    ",
                "OOWWRRYY",
                "YYOOWWRR",
                "  GG    ",
                "  GG    ",
            ],
            # action 5: axis=0, layer=1, rotate=2
            [
                "  BB    ",
                "  BB    ",
                "OOWWRRYY",
                "RRYYOOWW",
                "  GG    ",
                "  GG    ",
            ],
            # action 6: axis=1 (x轴), layer=0, rotate=-1
            [
                "  BY    ",
                "  BY    ",
                "OOWBRRGY",
                "OOWBRRGY",
                "  GW    ",
                "  GW    ",
            ],
            # action 7: axis=1, layer=0, rotate=1
            [
                "  BW    ",
                "  BW    ",
                "OOWGRRBY",
                "OOWGRRBY",
                "  GY    ",
                "  GY    ",
            ],
            # action 8: axis=1, layer=0, rotate=2
            [
                "  BG    ",
                "  BG    ",
                "OOWYRRWY",
                "OOWYRRWY",
                "  GB    ",
                "  GB    ",
            ],
            # action 9: axis=1, layer=1, rotate=-1
            [
                "  YB    ",
                "  YB    ",
                "OOBWRRYG",
                "OOBWRRYG",
                "  WG    ",
                "  WG    ",
            ],
            # action 10: axis=1, layer=1, rotate=1
            [
                "  WB    ",
                "  WB    ",
                "OOGWRRYB",
                "OOGWRRYB",
                "  YG    ",
                "  YG    ",
            ],
            # action 11: axis=1, layer=1, rotate=2
            [
                "  GB    ",
                "  GB    ",
                "OOYWRRYW",
                "OOYWRRYW",
                "  BG    ",
                "  BG    ",
            ],
            # action 12: axis=2 (z轴), layer=0, rotate=-1
            [
                "  BB    ",
                "  RR    ",
                "OBWWGRYY",
                "OBWWGRYY",
                "  OO    ",
                "  GG    ",
            ],
            # action 13: axis=2, layer=0, rotate=1
            [
                "  BB    ",
                "  OO    ",
                "OGWWBRYY",
                "OGWWBRYY",
                "  RR    ",
                "  GG    ",
            ],
            # action 14: axis=2, layer=0, rotate=2
            [
                "  BB    ",
                "  GG    ",
                "ORWWORYY",
                "ORWWORYY",
                "  BB    ",
                "  GG    ",
            ],
            # action 15: axis=2, layer=1, rotate=-1
            [
                "  OO    ",
                "  BB    ",
                "GOWWRBYY",
                "GOWWRBYY",
                "  GG    ",
                "  RR    ",
            ],
            # action 16: axis=2, layer=1, rotate=1
            [
                "  RR    ",
                "  BB    ",
                "BOWWRGYY",
                "BOWWRGYY",
                "  GG    ",
                "  OO    ",
            ],
            # action 17: axis=2, layer=1, rotate=2
            [
                "  GG    ",
                "  BB    ",
                "ROWWROYY",
                "ROWWROYY",
                "  GG    ",
                "  BB    ",
            ],
        ]
        for i, action in enumerate(actions):
            assert (
                action.get_dst().to_str() == expected[i]
            ), f"action {i} mismatch: {action.get_dst().to_str()} != {expected[i]}"

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

    def test_action_rotate_four_times_restore(self):
        """
        测试每个action旋转4次是否都能还原
        - rotate=1: 顺时针旋转1圈，旋转4次应还原（4*90°=360°）
        - rotate=-1: 逆时针旋转1圈，旋转4次应还原（4*(-90°)=(-360°)）
        - rotate=2: 旋转180度，旋转2次应还原（2*180°=360°），旋转4次也还原
        """
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
                    logger.error(
                        f"动作不存在: axis={axis}, layer={layer}, rotate={rotate}"
                    )
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

    # ---------- CubeState 补充测试 ----------

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

    def test_bfs_finds_solution(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s.get_sort_actions()[0].get_dst()
        states = scrambled.bfs(max_depth=3)
        solved = states.get(C.init_mask)
        self.expect(solved is not None, True)
        for a in solved[0]:
            scrambled = a.get_dst()
        self.expect(scrambled.game_over(), True)

    # ---------- CubeAction 补充测试 ----------

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

    # ---------- get_converts 单元测试 ----------

    def test_get_converts_unit(self):
        """
        直接测试 C.get_converts(mask, i, j, tp, grid) 的旋转逻辑。

        分析: get_converts 从原始 grid 读取颜色值,写入 mask 的新位偏移中。
        对于转环 a2=[p0,p1,p2,p3] 中的每个源位置 a(ii),其颜色 grid[a]
        被写入目标位置 a2[(ii+tp)%4]。
        all_size-1-x 的镜像是因为 encode_data 是 MSB-first 打包,
        而 set_mask 从 LSB 计数。

        以 axis=0, layer=0, tp=1 为例:
          环 [16,4,8,12]: 16→4(Yellow→Orange面), 4→8(Orange→White面),
                          8→12(White→Red面), 12→16(Red→Yellow面)
          环 [17,5,9,13]: 对应的 deeper strip 同理
          环 [0,1,2,3]: 顶面旋转,但因为初始全蓝色(0),无可见变化
        """
        s = CubeState.new_shape(C.SHAPE2)
        n = C.n
        BIT_SIZE = C.BIT_SIZE
        all_size = C.SIZE * n * n  # 24

        original_grid = s.grid.copy()
        original_mask = s.state

        # ---- axis=0, layer=0, tp=1 (y轴顺时针,顶层) ----
        r1 = C.get_converts(original_mask, 0, 0, 1, original_grid)
        g1 = decode_data(r1, [BIT_SIZE] * all_size)

        # 受影响的环: [0,1,3,2], [16,4,8,12], [17,5,9,13]
        rings_0_0 = {0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 16, 17}
        unchanged = set(range(all_size)) - rings_0_0

        # 验证: 不在环中的位置保持不变
        for pos in unchanged:
            self.expect(g1[pos], original_grid[pos], f"pos {pos} unchanged")

        # 环 [16,4,8,12]: 每个位置的颜色顺移到下一个
        # grid[16]=4→pos4, grid[4]=1→pos8, grid[8]=2→pos12, grid[12]=3→pos16
        self.expect(g1[4], 4, "pos4: Yellow from pos16")
        self.expect(g1[8], 1, "pos8: Orange from pos4")
        self.expect(g1[12], 2, "pos12: White from pos8")
        self.expect(g1[16], 3, "pos16: Red from pos12")

        # 环 [17,5,9,13]: 同理
        self.expect(g1[5], 4, "pos5: Yellow from pos17")
        self.expect(g1[9], 1, "pos9: Orange from pos5")
        self.expect(g1[13], 2, "pos13: White from pos9")
        self.expect(g1[17], 3, "pos17: Red from pos13")

        # ---- axis=0, layer=0, tp=-1 (y轴逆时针,顶层) ----
        rm1 = C.get_converts(original_mask, 0, 0, -1, original_grid)
        gm1 = decode_data(rm1, [BIT_SIZE] * all_size)

        # tp=-1 是顺时针反向: 源位置 a2[ii]→目标 a2[(ii-1)%4] = a2[(ii+3)%4]
        self.expect(gm1[12], 4, "pos12: Yellow from pos16 (ccw)")
        self.expect(gm1[16], 1, "pos16: Orange from pos4 (ccw)")
        self.expect(gm1[4], 2, "pos4: White from pos8 (ccw)")
        self.expect(gm1[8], 3, "pos8: Red from pos12 (ccw)")

        # ---- axis=0, layer=0, tp=2 (180°) ----
        r2 = C.get_converts(original_mask, 0, 0, 2, original_grid)
        g2 = decode_data(r2, [BIT_SIZE] * all_size)

        # tp=2: 位置互换, 对角线映射 a2[ii]→a2[(ii+2)%4]
        self.expect(g2[8], 4, "pos8: Yellow from pos16 (180)")
        self.expect(g2[12], 1, "pos12: Orange from pos4 (180)")
        self.expect(g2[16], 2, "pos16: White from pos8 (180)")
        self.expect(g2[4], 3, "pos4: Red from pos12 (180)")

        # ---- 逆操作验证: tp=1 后 tp=-1 应还原 ----
        r_apply = C.get_converts(original_mask, 0, 0, 1, original_grid)
        g_apply = decode_data(r_apply, [BIT_SIZE] * all_size)
        r_revert = C.get_converts(r_apply, 0, 0, -1, g_apply)
        g_revert = decode_data(r_revert, [BIT_SIZE] * all_size)
        self.expect(g_revert, original_grid, "tp=1 then tp=-1 restores")

        # ---- 180° 两次还原 ----
        once = C.get_converts(original_mask, 0, 0, 2, original_grid)
        g_once = decode_data(once, [BIT_SIZE] * all_size)
        twice = C.get_converts(once, 0, 0, 2, g_once)
        g_twice = decode_data(twice, [BIT_SIZE] * all_size)
        self.expect(g_twice, original_grid, "tp=2 twice restores")

        # ---- 层隔离: axis=0 layer=0 不影响 layer=1 的环 ----
        # layer=1 的环: [20,21,23,22], [10,14,18,6], [11,15,19,7]
        layer1_ring = {20, 21, 23, 22, 10, 14, 18, 6, 11, 15, 19, 7}
        for pos in layer1_ring:
            self.expect(g1[pos], original_grid[pos], f"layer1 pos {pos} unchanged by layer0")

        # ---- axis=1 (x轴), layer=0, tp=1 验证环映射 + 非环位不变 ----
        r_x = C.get_converts(original_mask, 1, 0, 1, original_grid)
        g_x = decode_data(r_x, [BIT_SIZE] * all_size)

        # (1,0) 的环: [12,13,15,14], [1,16,21,9], [3,18,23,11]
        # 环 [1,16,21,9]: pos1→16(Top→Back), pos16→21(Back→Bottom), pos21→9(Bottom→Front), pos9→1(Front→Top)
        self.expect(g_x[16], 0, "pos16: Blue from pos1 (top→back)")
        self.expect(g_x[21], 4, "pos21: Yellow from pos16 (back→bottom)")
        self.expect(g_x[9], 5, "pos9: Green from pos21 (bottom→front)")
        self.expect(g_x[1], 2, "pos1: White from pos9 (front→top)")
        # 环 [3,18,23,11]: pos3→18, pos18→23, pos23→11, pos11→3
        self.expect(g_x[18], 0, "pos18: Blue from pos3")
        self.expect(g_x[23], 4, "pos23: Yellow from pos18")
        self.expect(g_x[11], 5, "pos11: Green from pos23")
        self.expect(g_x[3], 2, "pos3: White from pos11")

        x_ring = {12, 13, 15, 14, 1, 16, 21, 9, 3, 18, 23, 11}
        x_unchanged = set(range(all_size)) - x_ring
        for pos in x_unchanged:
            self.expect(g_x[pos], original_grid[pos], f"x-axis unchanged pos {pos}")
