from app.tool.cube import CubeApi
from common.util.export import TestBase


class TestCubeApi(TestBase):
    @classmethod
    def setup_class(cls):
        cls.api = CubeApi()

    def test_new(self):
        result = self.api.new(n=2)
        self.expect(result.value["game_over"], True)
        self.expect(len(result.value["grid"]), 24)

    def test_random(self):
        result = self.api.random(steps=3)
        self.expect(result.value["game_over"], False)
        self.expect(len(result.childs), 3)

    def test_rotate(self):
        new_result = self.api.new(n=2)
        state = new_result.value["state"]

        rotate_result = self.api.rotate(state, 0, 0, 1)
        self.expect(rotate_result.value["game_over"], False)
        self.expect("action" in rotate_result.value, True)

    def test_solve(self):
        new_result = self.api.new(n=2)
        state = new_result.value["state"]

        # 不打乱，直接求解完成状态
        solve_result = self.api.solve(state)
        self.expect(solve_result.value["solved"], True)
        self.expect(solve_result.value["message"], "魔方已完成")

    def test_get_state(self):
        new_result = self.api.new(n=2)
        state = new_result.value["state"]

        get_result = self.api.get_state(state)
        self.expect(get_result.value["game_over"], True)
