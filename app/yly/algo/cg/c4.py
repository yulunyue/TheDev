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
        self.WINSCORE=[0,0]
        self.init_score()
        self.init_w()
        self.init_lines()


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
     
        # logger.info([bin(self.WINSCORE[0]),bin(self.WINSCORE[1])])

        
    def init_w(self):
        self.state_pos=[]
        
        for i in range(4):
            self.state_pos.append([
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


    def init_lines(self):
        self.line_num=0
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
                                self.line_num,idx
                            ])
                        self.line_num+=1

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
STORE_STATE:Dict[int,State]=dict()
class F4State(State):
    def __init__(self,mask,moves=0) -> None:
        self.mask = mask
        self.moves = moves
        self.score=0
        super().__init__()
    
    def init_root(self):
        self.line_state = [0]*C.line_num
        self.state = dict()
    def calc_value(self):
        return self.score if self.moves==1 else -self.score
    
    def put(self, col):
        mask0:int=(self.mask&C.HEIGHT_MASK1[col])<<1
        if mask0&C.HEIGHT_POS_MASK[col][0]:
            return
        mask1 = self.mask&C.HEIGHT_MASK0[col]
        if self.moves:
            mask1|=C.HEIGHT_POS_MASK[col][1]
        else:
            mask1&=C.HEIGHT_POS_MASK[col][2]
        mask = mask1|mask0
        if mask not in STORE_STATE:
            STORE_STATE[mask]=F4State(
                mask,1-self.moves
            ).init_state(
                col,(mask0.bit_length()-2)%C.HEIGHT,
                self.line_state,
                self.score,
                self.state
            )
        return STORE_STATE[mask]
    
    def init_state(self,x,y,line_state:List[int],score,state:dict):
        self.line_state=line_state.copy()
        self.state=state.copy()
        self.score=score
        for line_id,k_id in C.point_line_id[y][x]:
            old_state=self.line_state[line_id]
            self.state[old_state]=self.state.get(old_state,0)-1
            new_state=old_state|C.state_pos[k_id][self.moves]
            self.score+=C.score_map[new_state]-C.score_map[old_state]
            self.line_state[line_id]=new_state
            self.state[new_state]=self.state.get(new_state,0)+1
        return self


    def to_str(self,info="cur"):
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
        head = [
            f"----{info}--score:{self.score}--value:{self.value}--best:{self.best_action}----",
        ]        
        return "\n".join(head+["".join(v) for v in ret]+[
            "-"*12,
        ])

    def __str__(self):
        ret=self.to_str()
        best:F4State=self.get_end()
        if best:
            ret+="\n"+best.to_str("end")
        return ret
    
    def out_put(self,v):
        logger.info(f'put {self.col} {v}\n{self.to_str()}')


    def get_nexts(self, depth):
        if depth>=1:
            return []
        if not self.next_state:  
            for col in range(C.WIDTH):
                s=self.put(col)
                if s:
                    self.next_state[col]=s
        return self.next_state.items()




class Solution(SolutionBase):
    uri="https://www.codingame.com/ide/puzzle/connect-4"
    game_id = '70989246b492bcc523436cf43b6090c82395d392'
    agentsIds = [
        -2,-1
    ]
    name = 'f4'
    def get_cases(self):
        return [
            dict(result="xx",num=1,back=100),
        ]
    


    def init(self,**kw):
        self.state=F4State(C.INIT_MASK)
        self.state.init_root()
        self.seach=TreeSearch()
    

    def replay(self,stdout,back=1,**kw):
        i=0
        while i<len(stdout):
            self.state:State=self.state.put(int(stdout[i]))
            if i%2==0 and i+back>=len(stdout):
                self.seach.search(self.state)
                result=stdout[i+1] if i+1<len(stdout) else None
                self.log(f'round:{i}-cur:{stdout[i]}-result:{result}\n{self.state}')
            i+=1
            
        

    def dev(self,num=1,**kw):
        for i in range(num):
            self.seach.search(self.state)
            self.log(f'---round {i}----\n{self.state}')
            self.state=self.state.next_state[self.state.best_action]

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
                self.state:F4State=self.state.put(opp_previous_action)
            self.seach.search(self.state)
            self.output(self.state.best_action)
            self.state=self.state.next_state[self.state.best_action]
            




if __name__=='__main__':
    Solution().run()