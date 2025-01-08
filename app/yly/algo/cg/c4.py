from app.yly.algo.manage import SolutionBase,View
from common.algo.absearch import AlphaBateSearch,AbNode
from typing import Dict,List
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
HEIGHT=7
WIDTH=9
FOUR=4


class F4State(AbNode):
    def __init__(self,pos=0,mask=0,moves=0) -> None:
        self.pos = pos
        self.mask = mask
        self.moves = moves
        super().__init__()

    def put(self, pos):
        self.pos ^= self.mask
        self.mask |=self.mask +  1 << (pos * (HEIGHT + 1))
        self.moves+=1

    def make_move(self,move):
        return F4State(self.pos^self.mask,self.mask|move,self.moves+1)
    
    def print(self):
        ret=[]
        for i in range(HEIGHT-1,-1,-1):
            tmp=""
            for j in range(WIDTH):
                t=1<<((HEIGHT+1)*j+i)
                if self.mask & t:
                    if self.pos&t==(self.moves%2==0):
                        tmp+=" X"
                    else:
                        tmp+=" O"
                else:
                    tmp+=" -"
            ret.append(tmp)
        return "\n".join(ret)

class F4Serach(AlphaBateSearch):
    pass

class Solution(SolutionBase):
    uri="https://www.codingame.com/ide/puzzle/connect-4"
    game_id = '70989246b492bcc523436cf43b6090c82395d392'
    agentsIds = [
        -2,-1
    ]
    def get_cases(self):
        return [
            
            dict(board_rows='''.........
.........
.........
.........
10.......
10.......
10.......'''.split('\n'),result="")
        ]
    
    def init(self,board_rows):
        self.board_rows=board_rows
        self.state=F4State()
        ct=[[],[]]
        mv=0
        for w in self.board_rows[::-1]:
            if not w:
                continue

            for j,v in enumerate(w):
                if v=='.':
                    continue
                ct[int(v)].append(j)
                mv+=1
        
        for i in range(mv):
            cm=ct[i%2].pop()
            self.state.put(cm)    
                

    def search(self):
        self.log(self.state.print())


    def execute(self):
        pass

    def exec(self):
        my_id, opp_id = [int(i) for i in self.input().split()]
        # game loop
        while True:
            turn_index = int(self.input())  # starts from 0; As the game progresses, first player gets [0,2,4,...] and second player gets [1,3,5,...]
            board_rows=[]
            for i in range(7):
                board_rows.append(self.input())  # one row of the board (from top to bottom)
            num_valid_actions = int(self.input())  # number of unfilled columns in the board
            for i in range(num_valid_actions):
                action = int(self.input())  # a valid column index into which a chip can be dropped
            opp_previous_action = int(self.input())  # opponent's previous chosen column index (will be -1 for first player in the first turn)
            self.error("log")
            self.init(board_rows)
            self.output(self.execute())




if __name__=='__main__':
    Solution().run()