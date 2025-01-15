from app.yly.algo.manage import SolutionBase,View
from common.algo.absearch import AlphaBateSearch,AbNode
from typing import Dict,List
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")


class Constant:
    HEIGHT=7
    WIDTH=9
    FOUR=4
    def __init__(self) -> None:
        self.INIT_MASK=0
        self.MASK_FULL_HEIGHT=(1<<(self.HEIGHT+1))-1
        self.MASK_FULL=(1<<((self.HEIGHT+1)*self.WIDTH))-1
        self.HEIGHT_MASK0=[]
        self.HEIGHT_MASK1=[]
        self.HEIGHT_POS_MASK=[]
        self.init_w()

    def init_w(self):
        for col in range(self.WIDTH):
            pos=col*(self.HEIGHT+1)
            self.INIT_MASK|=1<<pos
            self.HEIGHT_POS_MASK.append([0,1<<pos])
            self.HEIGHT_MASK1.append(self.MASK_FULL_HEIGHT<<pos)
            self.HEIGHT_MASK0.append(self.MASK_FULL-self.HEIGHT_MASK1[-1])
    def print_str(self,mask):
        ret=[[" -"]*C.WIDTH for _ in range(self.HEIGHT)]
        for j in range(C.WIDTH):
            pos=j*(self.HEIGHT+1)
            h_mask:int=(mask>>pos)&self.MASK_FULL_HEIGHT
            l=h_mask.bit_length()-1
            for i in range(l):
                if h_mask&(1<<i):
                    ret[C.HEIGHT-(l-i)][j]=' X'
                else:
                    ret[C.HEIGHT-(l-i)][j]=' O'
            
        return "\n".join(["".join(v) for v in ret])

C=Constant()
class F4State(AbNode):
    store_state=dict()
    def __init__(self,mask,moves) -> None:
        self.mask = mask
        self.moves = moves
        self.score = -inf
        self.init()
        super().__init__()
    
    def init(self):
        pass

    
    def put(self, col):
        mask = (
            ((self.mask&C.HEIGHT_MASK1[col])<<1)|C.HEIGHT_POS_MASK[col][self.moves]
        )|(self.mask&C.HEIGHT_MASK0[col])
        if mask not in F4State.store_state:
            F4State.store_state[mask]=F4State(mask,1-self.moves)
        return F4State.store_state[mask]

    
  

    def get_nexts(self, depth):
        if depth>0 or self.value!=0:
            return []
        for col in range(C.WIDTH):
            pass


class F4Serach(AlphaBateSearch):
    def solve(self,b:F4State):
        if b.can_win_with_one_move():
            pass
    
    def get_move(self,b:F4State):
        move = b.get_winning_moves() & b.get_legal_moves()
        if move:
            return move & -move
        move_scores:List[F4State]=b.get_nexts()
        if not move_scores:
            move = b.get_legal_moves()
            return move & -move
        max=C.MIN_SCORE-1
        for mv in move_scores:
            if mv.score>max:
                max=mv.score
                move=mv.mask
        return mv
        
        

class Solution(SolutionBase):
    uri="https://www.codingame.com/ide/puzzle/connect-4"
    game_id = '70989246b492bcc523436cf43b6090c82395d392'
    agentsIds = [
        -2,-1
    ]
    name = 'f4'
    def get_cases(self):
        return [
            dict(result=""),
        ]
    


    def init(self, stderr=None,stdout=None,back=None,**kw):
        self.state=F4State(C.INIT_MASK,0)
        self.ab=F4Serach()
        if stdout and back:
            # self.log("\n".join(stderr[-1]["inputs"][1:8]))
            # self.log(f'out:{back}-> {stdout[back]}')
            for v in stdout[:back]:
                self.state=self.state.put(int(v))
    
    def dev(self):
        self.state:F4State=self.state.put(2).put(3).put(3)
        self.log(C.print_str(self.state.mask))

            
    def execute(self):
        self.ab.search(self.state)
        # self.log(self.state.best_action.value)
        col=self.state.best_action.col
        self.state=self.state.put(col)
        return col
    

    def exec(self):
        my_id, opp_id = [int(i) for i in self.input().split()]
        # game loop
        self.init()
        while True:
            turn_index = self.input()  # starts from 0; As the game progresses, first player gets [0,2,4,...] and second player gets [1,3,5,...]
            if turn_index is None:
                return
            board_rows=[]
            for i in range(7):
                board_rows.append(self.input())  # one row of the board (from top to bottom)
            num_valid_actions = int(self.input())  # number of unfilled columns in the board
            for i in range(num_valid_actions):
                action = int(self.input())  # a valid column index into which a chip can be dropped
            opp_previous_action = int(self.input())  # opponent's previous chosen column index (will be -1 for first player in the first turn)
            self.error(opp_previous_action=opp_previous_action)
            if opp_previous_action!=1:
                self.state=self.state.put(opp_previous_action)
            self.output(self.execute())




if __name__=='__main__':
    Solution().run()