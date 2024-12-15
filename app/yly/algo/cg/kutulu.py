from app.yly.algo.manage import SolutionBase

from typing import Dict,List
from functools import lru_cache
import math
MOD=(10**9)+7
inf = float("inf")
class Solution(SolutionBase):
    uri='https://www.codingame.com/ide/puzzle/code-of-kutulu'
    game_id="59755350863a5f654a8f27dc827b976824254c5b"
    agentsIds=[-1,-2,-2,-2]
    def get_cases(self):
        return [

        ]
    def init_grid(self,lines):
        pass
    
    def init(self,*args,**kwargs):
        pass
    
    def execute(self):
        pass
    
    def exec(self):
        # Survive the wrath of Kutulu
        # Coded fearlessly by JohnnyYuge & nmahoude (ok we might have been a bit scared by the old god...but don't say anything)
        self.width = int(self.input())
        self.height = int(self.input())
        self.init_grid([self.input() for _ in range(self.height)])
        # sanity_loss_lonely: how much sanity you lose every turn when alone, always 3 until wood 1
        # sanity_loss_group: how much sanity you lose every turn when near another player, always 1 until wood 1
        # wanderer_spawn_time: how many turns the wanderer take to spawn, always 3 until wood 1
        # wanderer_life_time: how many turns the wanderer is on map after spawning, always 40 until wood 1
        self.sanity_loss_lonely, self.sanity_loss_group, self.wanderer_spawn_time, self.wanderer_life_time = [int(i) for i in self.input().split()]
        # game loop
        while True:
            entity_count = int(self.input())  # the first given entity corresponds to your explorer
            for i in range(entity_count):
                inputs = self.input().split()
                entity_type = inputs[0]
                _id = int(inputs[1])
                x = int(inputs[2])
                y = int(inputs[3])
                param_0 = int(inputs[4])
                param_1 = int(inputs[5])
                param_2 = int(inputs[6])

            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr, flush=True)

            # MOVE <x> <y> | WAIT
            print(self.execute())


if __name__=='__main__':
    Solution().run()