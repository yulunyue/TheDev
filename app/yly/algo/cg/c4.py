from app.yly.algo.manage import SolutionBase,View,logger
from common.algo.search.base_search import TreeSearch,State
from common.algo.search.alphabate_search import ABNode,AlphaBateSearch
from collections import defaultdict
from typing import Dict,List
import socket
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
DR=[[0,1],[1,0],[1,1],[-1,1]]
def str_mid(s:str,size,fill="-"):
    if len(s)>=size:
        return s[:size]
    c=size-len(s)
    l,y=c//2,c%2
    return fill*l+s+fill*(l+y)
class Constant:
    HEIGHT=7
    WIDTH=9
    FOUR=4
    TRUN_INDEX=0
    O_FOUR=4
    X_FOUR=8
    O1_X3=9
    O3_X1=10
    def __init__(self) -> None:
        self.init_score()
        self.init_w()
        self.init_lines()

    def init_score(self):
        self.score_map=[0]*(1<<8)
        self.scores=[0,1,20,400,80000,-1,-20,-400,-80000,0,0,0,0]
        self.score2=[0]*15
        self.score2[self.O3_X1],self.score2[self.O1_X3]=-70000,70000
        for i in range(1<<8):
            ct=[0]*4
            s=i
            while s>0:
                ct[s&3]+=1
                s=s>>2
            if ct[3]:
                continue
            if ct[1]==1 and ct[2]==3:
                self.score_map[i]=self.O1_X3
            elif ct[1]==3 and ct[2]==1:
                self.score_map[i]=self.O3_X1
            elif ct[1]==0 and ct[2]:
                self.score_map[i]=4+ct[2]
            elif ct[2]==0 and ct[1]:
                self.score_map[i]=ct[1]
            else:
                self.score_map[i]=0
        
     
        # logger.info([bin(self.WINSCORE[0]),bin(self.WINSCORE[1])])

        
    def init_w(self):
        self.COLS=[4,3,5,2,6,1,7,0,8]
        self.MASK_FULL_HEIGHT=(1<<self.HEIGHT+1)-1
        self.MASK_FULL=(1<<((self.HEIGHT+1)*self.WIDTH))-1
        self.state_pos=[]
        self.INIT_MASK=0
        self.HEIGHT_MASK0=[]
        self.HEIGHT_MASK1=[]
        self.HEIGHT_POS_MASK=[]
        for i in range(4):
            self.state_pos.append([
                1<<(i*2),
                1<<(i*2+1),
                (1<<8)-1-(3<<(i*2))
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
            # logger.info([col,bin(pos_state<<self.HEIGHT)])
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

C=Constant()
STORE_STATE:Dict[int,State]=dict()
class F4State(ABNode):
    def __init__(self,mask,moves=0) -> None:
        self.mask = mask
        self.moves = moves
        self.score=0
        super().__init__()
    
    def init_root(self):
        self.line_state = [0]*C.line_num
        self.state = [0]*len(C.scores)

    def calc_value(self,depth):
        return self.score if self.moves%2==1 else -self.score
    
    def put(self, col):
        mask0:int=(self.mask&C.HEIGHT_MASK1[col])<<1
        if mask0&C.HEIGHT_POS_MASK[col][0]:
            return
        mask1 = self.mask&C.HEIGHT_MASK0[col]
        if self.moves%2==1:
            mask1|=C.HEIGHT_POS_MASK[col][1]
        else:
            mask1&=C.HEIGHT_POS_MASK[col][2]
        mask = mask1|mask0
        if mask not in STORE_STATE:
            STORE_STATE[mask],flag=F4State(
                mask,self.moves+1
            ).init_state(
                col,mask0.bit_length()-col*(C.HEIGHT+1)-2,
                self.line_state,
                self.score,
                self.state
            )
            if flag:
                self.next_state={col:STORE_STATE[mask]}
        return STORE_STATE[mask]

    def init_state(self,x,y,line_state:List[int],score,state:list):
        self.line_state=line_state.copy()
        self.state=state.copy()
        oo=False
        for line_id,k_id in C.point_line_id[y][x]:
            old_state=self.line_state[line_id]
            new_state=old_state|C.state_pos[k_id][self.moves%2]
            self.line_state[line_id]=new_state
            new_state_id,old_state_id=C.score_map[new_state],C.score_map[old_state]
            if new_state_id==C.X_FOUR or new_state_id==C.O_FOUR:
                self.next_state=dict()
                self.score=C.scores[new_state_id]
                return self,True
            if new_state_id==C.O3_X1 and self.moves%2==1:
                oo=True
                self.score=C.score2[new_state_id]
            elif new_state_id==C.O1_X3 and self.moves%2==0:
                oo=True
                self.score=C.score2[new_state_id]
            score+=C.scores[new_state_id]-C.scores[old_state_id]
            self.state[old_state_id]=self.state[old_state_id]-1
            self.state[new_state_id]=self.state[new_state_id]+1
        if not oo:
            self.score=score
        return self,oo
    
    def score_detail(self):
        return f'a:{self.best_action};s:{self.score}'

    def to_str(self):
        ret=[["- "]*C.WIDTH for _ in range(C.HEIGHT)]
        ret.append([f'{i} ' for i in range(C.WIDTH)])
        for j in range(C.WIDTH):
            pos=j*(C.HEIGHT+1)
            h_mask:int=(self.mask>>pos)&C.MASK_FULL_HEIGHT
            l=h_mask.bit_length()-1
            for i in range(l):
                k=C.HEIGHT-(l-i)
                if h_mask&(1<<i):
                    ret[k][j]='X '
                else:
                    ret[k][j]='O '
        return [str_mid(self.score_detail(),C.WIDTH*2)]+["".join(v) for v in ret]
            


    def __str__(self):
        bests=self.get_bests()
        tmp=[""]*(C.HEIGHT+2)
        for i,best in enumerate(bests):
            for j,v in  enumerate(best.to_str()):
                tmp[j]+=" # "+v
        return "\n".join(tmp)
    



    def get_nexts(self, depth):
        if depth==0:
            return []
        if self.next_state is None:
            st1=dict()
            for col in C.COLS:
                s:F4State=self.put(col)
                if s is None:
                    continue
                st1[col]=s
            self.next_state=st1
        return self.next_state.items()




class Solution(SolutionBase):
    uri="https://www.codingame.com/ide/puzzle/connect-4"
    game_id = '70989246b492bcc523436cf43b6090c82395d392'
    #log_mode = 'debug'
    agentsIds = [
        4820019,-1
    ]
    name = 'f4'
    def get_cases(self):
        return [
            #dict(search_type="tree_search",method="analyze"),
            dict(search_type="alpha_bate_search"),
        ]
    
    def init(self, search_type="alpha_bate_search",search_max_depth=5,**kw):
        self.search_max_depth=search_max_depth
        self.state=F4State(C.INIT_MASK)
        self.state.init_root()
        self.seach:AlphaBateSearch={
            'tree_search':TreeSearch,
            'alpha_bate_search':AlphaBateSearch,
        }[search_type]()
    

    def replay(self,stdout:List[str],stderr=None,
               replay_turn=None,
               **kw):
        C.TRUN_INDEX=0
        state_num=0
        while C.TRUN_INDEX<len(stdout):
            # self.seach.search(self.state,self.search_max_depth)
            action=int(stdout[C.TRUN_INDEX])
            self.log("; ".join([
                f'round:{C.TRUN_INDEX}',
                f'action:{action}',
                f'search_best_action:{self.state.best_action}',
                f'state_count:{self.seach.state_count}',
            ]))
            self.log(self.state)
            state_num+=self.seach.state_count
            self.state:F4State=self.state.put(action)
            C.TRUN_INDEX+=1
        self.log(f'round:{C.TRUN_INDEX},state_num:{state_num}')
        self.log(self.state)
    
    def analyze(self,stdout,**kw):
        C.TRUN_INDEX=0
        states=[self.state]
        while C.TRUN_INDEX<len(stdout):
            action=int(stdout[C.TRUN_INDEX])
            states.append(states[-1].put(action))
            C.TRUN_INDEX+=1
        for i in range(len(states)-1,-1,-1):
            s=states[i]
            if i==1 or i==len(states)-1:
                self.log(s)
        
            # self.seach.search(s,4)
            # for b in s.get_bests():
            #     self.log(b.self_win,b.op_win)
            # for depth in range(1,15):
            #     pass
        

    def exec(self,**kw):
        my_id, opp_id = [int(i) for i in self.input().split()]
        # game loop
        self.init()
        while True:
            C.TRUN_INDEX = int(self.input())  # starts from 0; As the game progresses, first player gets [0,2,4,...] and second player gets [1,3,5,...]
            board_rows=[]
            for i in range(7):
                board_rows.append(self.input())  # one row of the board (from top to bottom)
            num_valid_actions = int(self.input())  # number of unfilled columns in the board
            for i in range(num_valid_actions):
                action = int(self.input())  # a valid column index into which a chip can be dropped
            opp_previous_action = int(self.input())  # opponent's previous chosen column index (will be -1 for first player in the first turn)
           
            if 0<=opp_previous_action<C.WIDTH:
                self.state:F4State=self.state.put(opp_previous_action)
            # if my_id==1 and turn_index==1 and 3<=opp_previous_action<=6:
            #     self.output(-2)
            #     continue
            self.seach.search(self.state, self.search_max_depth)
            self.error(
                opp_previous_action=opp_previous_action,
                # state=str(self.state)
            )
            self.output(self.state.best_action)
            self.state=self.state.next_state[self.state.best_action]
            
            


if __name__=='__main__':
    Solution().run()