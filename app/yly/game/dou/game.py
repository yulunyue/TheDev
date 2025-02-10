from app.yly.game.gm import GameBase
from collections import defaultdict
from typing import List
import numpy as np
class Constant:
    def __init__(self):
        self.init_deck()

    def init_deck(self):
        self.deck = []
        for i in range(3, 15):
            self.deck.extend([i for _ in range(4)])
        self.deck.extend([17 for _ in range(4)])
        self.deck.extend([20, 30])

C=Constant()

class Player:
    def __init__(self,player_id,env):
        self.player_id=player_id
        self.env:GameEnv=env
        self.cards=[]
        self.card_map=defaultdict(int)
        self.card_play_action = []
    def gen_moves(self):
        self.gen_type_num_move()
    
    def add_cards(self,cards):
        self.cards.extend(cards)

    def gen_type_num_move(self):
        self.card_moves=[[] for _ in range(4)]
        for key,value in self.card_map.items():
            self.card_moves[value-1].append(key)

    def get_move_type(self):
        pass

class GameEnv(GameBase):
    def __init__(self, room_id):
        super().__init__(room_id)
        
    def reset(self,idx=0):
        self.cards=[]
        np.random.shuffle(C.deck)
        self.player_id=idx
        card_id=0
        self.players:List[Player]=[]
        for i in range(3):
            self.players.append(Player(i,self))
            card_num=20 if i==self.player_id else 17
            self.players[i].add_cards(C.deck[card_id:card_id+card_num])
            card_id+=card_num
        

    def test(self):
        self.reset()


if __name__=="__main__":
    GameEnv().test()