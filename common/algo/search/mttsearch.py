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


class MctsSearchTree(Algo):

    def load(self, player_size=2, **kw):
        self.player_size = player_size
        self.scalar = 1 / (2 * math.sqrt(2.0))  # 0.353553
        self.explore_ratio = 0
        return self

    def select(self, node: MctsNode):
        while node.expand_nodes:
            node = max(node.expand_nodes, key=lambda v: self.ucb_score(v))
        return node

    def expand(self, node: MctsNode):
        if node.untried_actions:
            child = node.untried_actions.pop()
            child.parent = node
            node.expand_nodes.append(child)
            return child
        return node

    def backpropagate(self, node: MctsNode, value):
        while node:
            node.visits += 1
            if node.depth % self.player_size == node.player_id:
                node.mct_value += value
            node = node.parent

    def simulate(self, cur: MctsNode):
        while True:
            if cur.done == 0:
                return 0
            if cur.done > 0:
                return 1 if cur.done - 1 == cur.depth % self.player_size else -1
            if not cur.get_actions():
                print(cur.parent)
                print(cur)
                raise Exception("gg")
            next_step = cur.get_random_action().dst
            next_step.parent = cur
            cur = next_step

    def ucb_score(self, node: MctsNode):
        if not node.visits:
            return inf
        exploit = node.mct_value / node.visits  # 平均值
        explore = math.sqrt(2.0 * math.log(node.parent.visits) / node.visits)
        return exploit + self.scalar * explore

    def search_main(self, action: Action, budget=1000, max_t=0.1, **kw):
        t = time.time()
        self.state_count = 0
        while self.state_count < budget or time.time() - t < max_t:
            leaf = self.select(action.dst)
            expanded_node = self.expand(leaf)
            result = self.simulate(expanded_node)
            self.backpropagate(expanded_node, result)
            self.state_count += 1
        vt = 0
        for a in action.dst.get_actions():
            if a.dst.visits > vt:
                vt = a.dst.visits
                action.dst.best_action = a
