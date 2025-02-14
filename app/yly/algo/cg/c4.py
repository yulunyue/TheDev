from app.yly.algo.manage import SolutionBase,View,logger
from common.algo.search.base_search import TreeSearch,State
from common.algo.search.alphabate_search import ABNode
from typing import Dict,List
import socket
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
        
        self.height_mask=(1<<8)-1
        self.state=dict()
        self.WINSCORE=[0,0]
        self.init_score()
        self.init_w()
        self.init_lines()
        self.reset()

    def init_score(self):
        self.score=0
        self.score_map={}
        scores=[0,1,10,100,1000]
        for i in range(self.height_mask+1):
            ct=[0]*4
            s=i
            while s>0:
                ct[s&3]+=1
                s=s>>2
            if ct[3]:
                continue
            score=0
            if ct[1]==0 and ct[2]:
                score=-scores[ct[2]]
                if ct[2]==4:
                    self.WINSCORE[1]=i
            if ct[2]==0 and ct[1]:
                score=scores[ct[1]]
                if ct[1]==4:
                    self.WINSCORE[0]=i
            self.score_map[i]=score
            self.state[i]=0
        # logger.info([bin(self.WINSCORE[0]),bin(self.WINSCORE[1])])
    def get_state(self):
        if self.state[self.WINSCORE[0]]:
            return "O WIN"
        if self.state[self.WINSCORE[1]]:
            return "X WIn"
        
    def init_w(self):
        self.state_pos=[]
        
        for i in range(4):
            self.state_pos.append([
                self.height_mask-(3<<(i*2)),
                1<<(i*2),
                1<<(i*2+1)
            ])

        for col in range(self.WIDTH):
            pos=col*(self.HEIGHT+1)
            pos_state=1<<pos
            self.INIT_MASK|=1<<pos
            self.HEIGHT_POS_MASK.append([
                pos_state<<(self.HEIGHT+1),
                pos_state,
                self.MASK_FULL-pos_state
            ])
            self.HEIGHT_MASK1.append(self.MASK_FULL_HEIGHT<<pos)
            self.HEIGHT_MASK0.append(self.MASK_FULL-self.HEIGHT_MASK1[-1])

    def reset(self):
        
        self.pos=[0]*self.WIDTH

    def put(self,x,val):
        for line_id,k_id in self.point_line_id[self.pos[x]][x]:
            old_state=self.line_state[line_id]
            self.state[old_state]=self.state[old_state]-1
            if val:
                state=old_state|self.state_pos[k_id][val]
            else:
                state=old_state&self.state_pos[k_id][0]
            self.score+=self.score_map[state]-self.score_map[old_state]
            self.line_state[line_id]=state
            self.state[state]=self.state[state]+1
        
    
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
        ret=[f'score:{self.score}']
        for k1,v in self.state.items():
            if v<=0:
                continue
            s=["-"]*4
            k = k1
            i=0
            while k:
                s[i]=['-','O','X','?'][k&3]
                k=k>>2
                i+=1
            ret.append(f'{"".join(s[:])} -> {k1} -> {v}')
        return ret
    

                    

C=Constant()
class F4State(State):
    store_state=dict()
    def __init__(self,mask,moves=1,col=None) -> None:
        self.mask = mask
        self.moves = moves
        self.col=None
        super().__init__()
    
    def calc_value(self):
        self.value = C.score if self.moves==0 else -C.score
        return self.value
    
    def put(self, col):
        mask0=(self.mask&C.HEIGHT_MASK1[col])<<1
        if mask0&C.HEIGHT_POS_MASK[col][0]:
            return
        mask1 = self.mask&C.HEIGHT_MASK0[col]
        if self.moves:
            mask1|=C.HEIGHT_POS_MASK[col][1]
        else:
            mask1&=C.HEIGHT_POS_MASK[col][2]
        mask = mask1|mask0
        if mask not in F4State.store_state:
            F4State.store_state[mask]=F4State(mask,1-self.moves)
        F4State.store_state[mask].col=col
        return F4State.store_state[mask]

    def do(self):
        C.put(self.col,self.moves+1)
        C.pos[self.col]+=1
        # self.out_put(self.moves+1)
        

    def undo(self):
        C.pos[self.col]-=1
        C.put(self.col,0)

    def to_str(self):
        ret=[[" -"]*C.WIDTH for _ in range(C.HEIGHT)]

        for j in range(C.WIDTH):
            pos=j*(C.HEIGHT+1)
            h_mask:int=(self.mask>>pos)&C.MASK_FULL_HEIGHT
            l=h_mask.bit_length()-1
            for i in range(l):
                k=C.HEIGHT-(l-i)
                if h_mask&(1<<i):
                    ret[k][j]=' O'
                else:
                    ret[k][j]=' X'
        head = [
            "-"*12,
            f'value:{self.value}',
        ]
        if self.value:
            head+=C.to_str()
        return "\n".join(head+["".join(v) for v in ret]+[
            "-"*12,
        ])
    
    def out_put(self,v):
        logger.info(f'put {self.col} {v}\n{self.to_str()}')


    def get_nexts(self, depth):
        if depth>=1:
            return []
        ret=[]
        for col in range(C.WIDTH):
            s=self.put(col)
            if s:
                ret.append(s)
        return ret




class Solution(SolutionBase):
    uri="https://www.codingame.com/ide/puzzle/connect-4"
    game_id = '70989246b492bcc523436cf43b6090c82395d392'
    agentsIds = [
        -2,-1
    ]
    name = 'f4'
    def get_cases(self):
        return [
            dict(result="xx",num=1000,back=100),
        ]
    


    def init(self,**kw):
        self.state=F4State(C.INIT_MASK)
        self.seach=TreeSearch()
    

    def replay(self,stdout,back=1,**kw):
        i=0
        self.log(stdout)
        while i<len(stdout):
            self.state:State=self.state.put(int(stdout[i]))
            self.state.do()
            if i%2==0 and i+back>=len(stdout):
                self.log(self.state.to_str())
                self.seach.search(self.state)
                self.log(f'-{i}-{self.state.best_state.col}-')
                self.log(self.state.get_end().to_str())
                
            i+=1
            
        

    def dev(self,num=1,**kw):
        for _ in range(num):
            self.execute()
            game_state=C.get_state()
            if game_state:
                self.log(f"game_over {game_state}")
                break
        self.log(self.state.to_str())
       


            

    

    def exec(self,**kw):
        my_id, opp_id = [int(i) for i in self.input().split()]
        # game loop
        self.init()
        while True:
            turn_index = self.input()  # starts from 0; As the game progresses, first player gets [0,2,4,...] and second player gets [1,3,5,...]
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
                self.state.do()
            self.seach.search(self.state)
            self.state.best_state.do()
            self.output(self.state.best_state.col)
            




if __name__=='__main__':
    Solution().run()