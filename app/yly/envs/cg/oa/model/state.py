from common.algo.search.state import State, Action
from common.algo.learn.sarse.mctssearch import MctsState
from common.algo.search.state import Action
from common.algo.search.algo import Algo
from common.util.export import List
from app.yly.envs.cg.oa.model.constant import C


class StateBase(MctsState):

    STATE_MAP = dict()

    def __init__(self, state=None):
        super().__init__(state)
        self.current_round, self.score, *boards = C.decode_data(state)
        self.boards = [boards[: C.SELF_NUM], boards[C.SELF_NUM :]]
        self.nums = [sum(self.boards[0]), sum(self.boards[1])]
        self.op_score = C.ALL_SCORE - self.score - self.nums[0] - self.nums[1]
        self.reward = (self.score - self.op_score) / C.ALL_SCORE
        if self.score >= C.WIN_SCORE:
            self.reward = 1
            self.done = True
        elif self.op_score >= C.WIN_SCORE:
            self.reward = -1
            self.done = True
        elif self.nums[0] == 0 or self.current_round >= C.MAX_ROUND:
            self.done = True

    def get_reward(self, *args, **kw):
        return self.reward

    def make_actions(self, *args, **kw):
        actions = dict()
        for i in range(C.SELF_NUM):
            if self.boards[0][i] == 0:
                continue
            op_score = self.op_score
            rv_num = 0
            boards = [self.boards[0].copy(), self.boards[1].copy()]
            nums = [self.nums[0], self.nums[1]]
            idx = i
            player_id = 0
            boards[0][i] = 0

            for _ in range(self.boards[0][i]):
                idx += 1
                if idx == 6:
                    player_id = 1 - player_id
                    idx = 0
                if idx == i and player_id == 0:
                    idx += 1
                    if idx == 6:
                        player_id = 1 - player_id
                        idx = 0
                boards[player_id][idx] += 1
                nums[player_id] += 1

            while player_id == 1 and idx >= 0 and 2 <= boards[1][idx] <= 3:
                nums[1] -= boards[1][idx]
                rv_num += boards[1][idx]
                boards[1][idx] = 0
                idx -= 1
            if nums[1] == 0:
                continue
            if nums[0] == 0:
                op_score += nums[1]
                nums[1] = 0
                boards[1] = [0] * 6

            s = C.encode_data(self.current_round + 1, op_score, boards[1] + boards[0])
            actions[i] = Action(self, i, self.__class__.new(s)).set_reward(rv_num)
        return actions

    def get_depth_reward(self, depth, *args, **kw):
        return self.get_reward()

    def get_done(self):
        return self.done or not self.get_actions()
