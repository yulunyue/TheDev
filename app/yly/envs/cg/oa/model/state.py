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
        self.boards = boards[: C.SELF_NUM]
        self.op_boards = boards[C.SELF_NUM :]
        self.nums = sum(self.boards)
        self.op_nums = sum(self.op_boards)
        self.op_score = C.ALL_SCORE - self.score - self.nums - self.op_nums
        self.reward = (self.score - self.op_score) / C.ALL_SCORE
        if self.score >= C.WIN_SCORE:
            self.done = self.reward = 1
        elif self.op_score >= C.WIN_SCORE:
            self.done = self.reward = -1
        elif self.current_round >= C.MAX_ROUND:
            if self.score == self.op_score:
                self.done = 0
            elif self.score < self.op_score:
                self.done = -1
            else:
                self.done = 1

    def get_reward(self, *args, **kw):
        return self.reward

    def make_actions(self, *args, **kw):
        actions = dict()
        for i in range(C.SELF_NUM):
            if self.boards[i] == 0:
                continue
            score, op_score = self.score, self.op_score
            boards, op_boards = self.boards.copy(), self.op_boards.copy()
            nums, op_nums = self.nums - self.boards[i], self.op_nums
            idx = i
            is_self = True
            boards[i] = 0
            for _ in range(self.boards[i]):
                idx += 1
                if idx == 6:
                    boards, op_boards = op_boards, boards
                    nums, op_nums = op_nums, nums
                    is_self = not is_self
                    idx = 0
                if idx == i and is_self:
                    continue
                boards[idx] += 1
                nums += 1

            while not is_self and 2 <= boards[idx] <= 3:
                idx -= 1
                if idx == -1:
                    break
                op_nums -= boards[idx]
                score += boards[idx]
                boards[idx] = 0
            if not is_self:
                boards, op_boards = op_boards, boards
                nums, op_nums = op_nums, nums

            s = C.encode_data(self.current_round + 1, op_score, op_boards + boards)
            actions[i] = Action(self, i, self.__class__.new(s)).set_reward(
                score - self.score
            )
        return actions
