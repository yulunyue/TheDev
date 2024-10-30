

from typing import List, Dict, Optional
from collections import defaultdict, deque, Counter
from itertools import accumulate, product, permutations
from functools import lru_cache
import json
import bisect
import sys
import math
import heapq
inf = float("inf")
MOD = (10**9)+7
try:
    from app.yly.manage import SolutionBase
    DEV = True
except:
    DEV = False

    class SolutionBase:
        def input(self):
            return input()

        def log(self, info):
            print(json.dumps(info), file=sys.stderr, flush=True)

        def execute(self, *args, **kwargs):
            pass

        def run(self):
            while True:
                inp = input().split()
                x, y, next_x, next_y, next_checkpoint_dist, next_checkpoint_angle = [
                    int(l) for l in inp]
                opponent_x, opponent_y = [int(i) for i in input().split()]
                dst_x, dst_y, power = self.execute(x, y, next_x, next_y, next_checkpoint_dist,
                                                   next_checkpoint_angle, opponent_x, opponent_y)

                print(f'{dst_x} {dst_y} {power}')


class Agent:
    def __init__(self) -> None:
        self.p = 0.02
        self.i = 0
        self.d = 0
        self.i_sum = 0
        self.ai = 1.6
        self.last_d = None
        self.round = 0

    def calc(self, src_x, src_y, dst_x, dst_y, distance, next_checkpoint_angle, opponent_x, opponent_y):
        self.src_x = src_x
        self.src_y = src_y
        self.dst_x = dst_x
        self.dst_y = dst_y
        self.distance = distance
        self.i_sum += distance
        self.angle = abs(next_checkpoint_angle)**self.ai
        if self.last_d is None:
            d_cha = 0
        else:
            d_cha = distance-self.last_d
        power = int(self.distance*self.p+self.i *
                    self.i_sum+d_cha*self.d+self.angle)
        self.last_d = distance
        if self.round > 15:
            power = 0
        else:
            power = 100
        self.round += 1
        return self.dst_x, self.dst_y, max(min(power, 100), 0)


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/mad-pod-racing"
    gameid = '595803248f16a6655bc56f0b970000a821ea4db0'
    name = 'mad_pod'
    game_type = 'pk'
    agentsIds = [-2, -1]

    @classmethod
    def get_info(cls, **kw):
        return dict()

    def __init__(self) -> None:
        super().__init__()
        self.ai = Agent()

    def get_cases(self):
        return [

        ]

    def execute(self, src_x, src_y, dst_x, dst_y, distance, next_checkpoint_angle, opponent_x, opponent_y):
        return self.ai.calc(src_x, src_y, dst_x, dst_y, distance, next_checkpoint_angle, opponent_x, opponent_y)


if __name__ == '__main__':
    Solution().run()
