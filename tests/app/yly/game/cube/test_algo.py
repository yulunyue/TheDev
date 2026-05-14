from common.util.export import TestBase
from app.yly.envs.game.cube.model import CubeState
from app.yly.envs.game.cube.constant import C


class TestAlgo(TestBase):
    @classmethod
    def setup_class(cls):
        CubeState.STATE_STORE = {}
        cls.init_state = CubeState.new_shape(C.SHAPE2)

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

    def test_bfs_finds_solution(self):
        s = CubeState.new_shape(C.SHAPE2)
        scrambled = s.get_sort_actions()[0].get_dst()
        states = scrambled.bfs(max_depth=3)
        solved = states.get(C.init_mask)
        self.expect(solved is not None, True)
        for a in solved[0]:
            scrambled = a.get_dst()
        self.expect(scrambled.game_over(), True)
