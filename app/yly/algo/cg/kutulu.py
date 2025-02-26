from common.algo.manage import SolutionBase
from common.algo.graph import Graph
from typing import Dict,List
from functools import lru_cache
import math
MOD=(10**9)+7
inf = float("inf")
DR = [[1,0],[-1,0],[0,1],[0,-1]]
class Player:
    EXPLORER='EXPLORER'
    WANDERER='WANDERER'
    def __init__(self,entity_type,key,x,y,param_0,param_1,param_2) -> None:
        self.x=int(x)
        self.y=int(y)
        self.entity_type = entity_type
        self.key=key

class Solution(SolutionBase):
    name = "kutulu"
    uri='https://www.codingame.com/ide/puzzle/code-of-kutulu'
    game_id="59755350863a5f654a8f27dc827b976824254c5b"
    agentsIds=[-1,-2,-2,-2]
    def get_cases(self):
        return [

        ]
    
    def get_dis(self,c1,c2:Player):
        ret = self.grid.get_dis(c1,(c2.y,c2.x))
        return 0 if ret==inf else ret
    
    def execute(self):
        self.cur_node=self.node_map[Player.EXPLORER][0]
        ret=None
        dis_min=-inf

        for nk,*args in self.grid.g[(self.cur_node.y,self.cur_node.x)]:
            self.dis_w=[]
            self.dis_e=[]
            for w in self.node_map[Player.WANDERER]:
                self.dis_w.append(self.get_dis(nk,w))
            for e in self.node_map[Player.EXPLORER][1:]:
                self.dis_e.append(self.get_dis(nk,e))
            score = self.get_score()
            if score>dis_min:
                ret=nk
                dis_min=score
        return ret
    
    def get_score(self):
        min_w=min(self.dis_w)
        min_e=min(self.dis_e)
    
    def exec(self):
        # Survive the wrath of Kutulu
        # Coded fearlessly by JohnnyYuge & nmahoude (ok we might have been a bit scared by the old god...but don't say anything)
        
        self.nodes_list:list[Player]=[]
        self.width = int(self.input())
        self.height = int(self.input())
        self.grid = Graph().load_grid([self.input() for _ in range(self.height)])
        for key in self.grid.g.keys():
            self.grid.get_dis(key,None)
        # sanity_loss_lonely: how much sanity you lose every turn when alone, always 3 until wood 1
        # sanity_loss_group: how much sanity you lose every turn when near another player, always 1 until wood 1
        # wanderer_spawn_time: how many turns the wanderer take to spawn, always 3 until wood 1
        # wanderer_life_time: how many turns the wanderer is on map after spawning, always 40 until wood 1
        self.sanity_loss_lonely, self.sanity_loss_group, self.wanderer_spawn_time, self.wanderer_life_time = [int(i) for i in self.input().split()]
        # game loop
        while True:
            c=self.input()
            if not c:
                break
            entity_count = int(c)  # the first given entity corresponds to your explorer
            self.nodes_list:List[Player]=[]
            self.node_map:Dict[str,List[Player]] = {Player.EXPLORER:[],Player.WANDERER:[]}
            for _ in range(entity_count):
                inputs = self.input().split()
                p=Player(*inputs)
                self.nodes_list.append(p)
                self.node_map[p.entity_type].append(p)
            self.error()
            info=self.execute()
            if info:
                self.output(f'MOVE {info[1]} {info[0]}')
            else:
                self.output('WAIT')

if __name__=='__main__':
    Solution().run()