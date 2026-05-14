from common.algo.export import decode_data
from common.util.export import TestBase
from app.yly.envs.game.cube.model import CubeState
from app.yly.envs.game.cube.constant import C


class TestConvert(TestBase):
    @classmethod
    def setup_class(cls):
        CubeState.STATE_STORE = {}
        cls.init_state = CubeState.new_shape(C.SHAPE2)

    def test_get_converts_unit(self):
        s = CubeState.new_shape(C.SHAPE2)
        n = C.n
        BIT_SIZE = C.BIT_SIZE
        all_size = C.SIZE * n * n

        original_grid = s.grid.copy()
        original_mask = s.state

        r1 = C.get_converts(original_mask, 0, 0, 1, original_grid)
        g1 = decode_data(r1, [BIT_SIZE] * all_size)

        rings_0_0 = {0, 1, 2, 3, 4, 5, 8, 9, 12, 13, 16, 17}
        unchanged = set(range(all_size)) - rings_0_0

        for pos in unchanged:
            self.expect(g1[pos], original_grid[pos], f"pos {pos} unchanged")

        self.expect(g1[4], 4, "pos4: Yellow from pos16")
        self.expect(g1[8], 1, "pos8: Orange from pos4")
        self.expect(g1[12], 2, "pos12: White from pos8")
        self.expect(g1[16], 3, "pos16: Red from pos12")

        self.expect(g1[5], 4, "pos5: Yellow from pos17")
        self.expect(g1[9], 1, "pos9: Orange from pos5")
        self.expect(g1[13], 2, "pos13: White from pos9")
        self.expect(g1[17], 3, "pos17: Red from pos13")

        rm1 = C.get_converts(original_mask, 0, 0, -1, original_grid)
        gm1 = decode_data(rm1, [BIT_SIZE] * all_size)

        self.expect(gm1[12], 4, "pos12: Yellow from pos16 (ccw)")
        self.expect(gm1[16], 1, "pos16: Orange from pos4 (ccw)")
        self.expect(gm1[4], 2, "pos4: White from pos8 (ccw)")
        self.expect(gm1[8], 3, "pos8: Red from pos12 (ccw)")

        r2 = C.get_converts(original_mask, 0, 0, 2, original_grid)
        g2 = decode_data(r2, [BIT_SIZE] * all_size)

        self.expect(g2[8], 4, "pos8: Yellow from pos16 (180)")
        self.expect(g2[12], 1, "pos12: Orange from pos4 (180)")
        self.expect(g2[16], 2, "pos16: White from pos8 (180)")
        self.expect(g2[4], 3, "pos4: Red from pos12 (180)")

        r_apply = C.get_converts(original_mask, 0, 0, 1, original_grid)
        g_apply = decode_data(r_apply, [BIT_SIZE] * all_size)
        r_revert = C.get_converts(r_apply, 0, 0, -1, g_apply)
        g_revert = decode_data(r_revert, [BIT_SIZE] * all_size)
        self.expect(g_revert, original_grid, "tp=1 then tp=-1 restores")

        once = C.get_converts(original_mask, 0, 0, 2, original_grid)
        g_once = decode_data(once, [BIT_SIZE] * all_size)
        twice = C.get_converts(once, 0, 0, 2, g_once)
        g_twice = decode_data(twice, [BIT_SIZE] * all_size)
        self.expect(g_twice, original_grid, "tp=2 twice restores")

        layer1_ring = {20, 21, 23, 22, 10, 14, 18, 6, 11, 15, 19, 7}
        for pos in layer1_ring:
            self.expect(
                g1[pos], original_grid[pos], f"layer1 pos {pos} unchanged by layer0"
            )

        r_x = C.get_converts(original_mask, 1, 0, 1, original_grid)
        g_x = decode_data(r_x, [BIT_SIZE] * all_size)

        self.expect(g_x[16], 0, "pos16: Blue from pos1 (top->back)")
        self.expect(g_x[21], 4, "pos21: Yellow from pos16 (back->bottom)")
        self.expect(g_x[9], 5, "pos9: Green from pos21 (bottom->front)")
        self.expect(g_x[1], 2, "pos1: White from pos9 (front->top)")

        self.expect(g_x[18], 0, "pos18: Blue from pos3")
        self.expect(g_x[23], 4, "pos23: Yellow from pos18")
        self.expect(g_x[11], 5, "pos11: Green from pos23")
        self.expect(g_x[3], 2, "pos3: White from pos11")

        x_ring = {12, 13, 15, 14, 1, 16, 21, 9, 3, 18, 23, 11}
        x_unchanged = set(range(all_size)) - x_ring
        for pos in x_unchanged:
            self.expect(g_x[pos], original_grid[pos], f"x-axis unchanged pos {pos}")
