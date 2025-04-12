from common.algo.search.state import State, Action
from common.algo.search.algo import Algo
from typing import List, Dict
import math
import random
import numpy as np
import time

inf = float("inf")


class MctsNode(State):
    FIRST_PLAYER = 0

    def __init__(self, player_id, depth):
        super().__init__(player_id, depth)
        self.visits = 0
        self.vt_num = 0
        self.mct_value = 0  # 累计胜利值（玩家视角）
        self.expand_nodes: List[MctsNode] = []
        self.parent: MctsNode = None
        self._untried_actions: List[MctsNode] = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = [a.dst for a in self.get_actions()]
        return self._untried_actions

    # def get_random_action(self) -> Action:
    #     k = len(self.expand_nodes)
    #     return self.actions[np.random.randint(0, k)]


class MctsSearchTree(Algo):

    def load(self, player_size=2, max_t=-1, num_episodes=1000):
        self.player_size = player_size
        self.scalar = 1 / (2 * math.sqrt(2.0))  # 0.353553
        self.explore_ratio = 0
        return super().load(max_t=max_t, num_episodes=num_episodes)

    def select(self, node: MctsNode):
        while node.expand_nodes:
            node = max(node.expand_nodes, key=lambda v: self.ucb_score(v))
        return node

    def expand(self, node: MctsNode):
        if node.untried_actions:
            child = node.untried_actions.pop(0)
            node.expand_nodes.append(child)

    def backpropagate(self, node: MctsNode, value):
        while node:
            node.visits += 1
            if node.depth % self.player_size == node.player_id:
                node.mct_value += value
            node = node.parent

    def simulate(self, cur: MctsNode):
        p = cur
        while cur.done < 0:
            self.expand(cur)
            next_step = self.select(cur)
            next_step.parent = cur
            cur = next_step
        ret = 0
        if cur.done > 0:
            if cur.done - 1 == p.depth % self.player_size:
                ret = 1
            else:
                ret = -1
        return (cur, ret)

    def ucb_score(self, node: MctsNode):
        if not node.visits or node.parent is None:
            return inf
        exploit = node.mct_value / node.visits  # 平均值
        explore = math.sqrt(2.0 * math.log(node.parent.visits) / node.visits)
        return exploit + self.scalar * explore

    def search_main(self, action: Action):
        self.state_count = 0
        while self.state_count < self.num_episodes or (
            self.max_t > 0 and time.time() - self.begin_time < self.max_t
        ):
            node, result = self.simulate(action.dst)
            self.backpropagate(node, result)
            self.state_count += 1

        actions = action.dst.get_actions()
        actions.sort(key=lambda a: -a.dst.visits)
        action.dst.best_action = actions[0]
