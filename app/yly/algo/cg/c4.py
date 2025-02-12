from app.yly.algo.manage import SolutionBase,View
from common.algo.search.base_search import AlphaBateSearch,AbNode
from typing import Dict,List
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
DR=[[0,1],[1,0],[1,1],[-1,1]]
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
        self.init_score()
        self.init_w()
        self.init_lines()
        self.reset()
    def init_score(self):
        self.score=0
        self.score_map={
            0x01010101:100,
            0x10101010:-100
        }
    def init_w(self):
        self.state_pos=[]
        height_mask=(1<<4)-1
        for i in range(4):
            self.state_pos.append([
                height_mask-3<<(i*2),
                1<<(i*2),
                1<<(i*2+1)
            ])
        for col in range(self.WIDTH):
            pos=col*(self.HEIGHT+1)
            self.INIT_MASK|=1<<pos
            self.HEIGHT_POS_MASK.append([0,1<<pos])
            self.HEIGHT_MASK1.append(self.MASK_FULL_HEIGHT<<pos)
            self.HEIGHT_MASK0.append(self.MASK_FULL-self.HEIGHT_MASK1[-1])

    def reset(self):
        self.state={0:3<<4}
        self.pos=[0]*self.WIDTH

    def put(self,x,val):
        for line_id,k_id in self.point_line_id[self.pos[x]][x]:
            old_state=self.line_state[line_id]
            self.state[old_state]=self.state.get(old_state,0)-1
            if val:
                state=old_state|self.state_pos[k_id][val]
            else:
                state=old_state&self.state_pos[k_id][0]
            self.score+=self.score_map.get(state,0)-self.score_map.get(old_state,0)
            self.line_state[line_id]=state
            self.state[state]=self.state.get(state,0)+1
        self.pos[x]+=1 if val!=0 else -1
    
    def init_lines(self):
        self.line_state=[]
        self.point_line_id=[[
            [] for _ in range(self.WIDTH)
        ] for _ in range(self.HEIGHT)]
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                for y,x in DR:
                    tmp=[]
                    for k in range(4):
                        y1,x1=i+k*y,j+k*x
                        if 0<=y1<self.HEIGHT and 0<=x1<self.WIDTH:
                            tmp.append([y1,x1,k])
                    if len(tmp)==4:
                        for y1,x1,idx in tmp:
                            self.point_line_id[y1][x1].append([
                                len(self.line_state),idx
                            ])
                        self.line_state.append(0)

    def to_str(self):
        ret=[]
        for k1,v in self.state.items():
            if not v:
                continue
            s=["-"]*4
            k = k1
            i=0
            while k:
                s[i]=['-','O','X'][k&3]
                k=k>>2
                i+=1
            ret.append(f'{"".join(s[:])} -> {k1} -> {v}')
        return "\n".join(ret)
                 
                    

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
            (
                (self.mask&C.HEIGHT_MASK1[col])<<1
            )|C.HEIGHT_POS_MASK[col][self.moves]
        )|(self.mask&C.HEIGHT_MASK0[col])
        if mask not in F4State.store_state:
            F4State.store_state[mask]=F4State(mask,1-self.moves)
        C.put(col,self.moves+1)
        return F4State.store_state[mask]

    
    def to_str(self):
        ret=[[" -"]*C.WIDTH for _ in range(C.HEIGHT)]

        for j in range(C.WIDTH):
            pos=j*(C.HEIGHT+1)
            h_mask:int=(self.mask>>pos)&C.MASK_FULL_HEIGHT
            l=h_mask.bit_length()-1
            for i in range(l):
                k=C.HEIGHT-(l-i)
                if h_mask&(1<<i):
                    ret[k][j]=' X'
                else:
                    ret[k][j]=' O'
            
        return "\n".join([C.to_str()]+["".join(v) for v in ret])
  

    def get_nexts(self, depth):
        if depth>0 or self.value!=0:
            return []
        for col in range(C.WIDTH):
            pass


class F4Serach(AlphaBateSearch):
    def solve(self,b:F4State):
        pass
    


class Solution(SolutionBase):
    uri="https://www.codingame.com/ide/puzzle/connect-4"
    game_id = '70989246b492bcc523436cf43b6090c82395d392'
    agentsIds = [
        -2,-1
    ]
    name = 'f4'
    def get_cases(self):
        return [
            dict(result="xx"),
        ]
    


    def init(self, stderr=None,stdout=None,back=None,**kw):
        self.state=F4State(C.INIT_MASK,0)
        self.ab=F4Serach()
        if stdout and back:
            # self.log("\n".join(stderr[-1]["inputs"][1:8]))
            # self.log(f'out:{back}-> {stdout[back]}')
            for v in stdout[:back]:
                self.state=self.state.put(int(v))
    
    def dev(self,**kw):
        for _ in range(3):
            self.state:F4State=self.state.put(1)
            self.state = self.state.put(0)
        self.log(self.state.to_str())
        # self.log(self.execute())

            
    def execute(self,**kw):
        self.ab.search(self.state)
        # self.log(self.state.best_action.value)
        col=self.state.best_action.col
        self.state=self.state.put(col)
        return col
    

    def exec(self,**kw):
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