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
        self.BOTTOM=0
        self.FULL=0
        self.HEIGHT_MASK=(1 << self.HEIGHT) - 1
        self.CLOUMN_MASK=[]
        self.init_w()
    def init_w(self):
        for i in range(self.WIDTH):
            pos=i*(self.HEIGHT+1)
            self.BOTTOM += 1<<pos
            self.FULL+=self.HEIGHT_MASK << pos
            self.CLOUMN_MASK.append(((1 << self.HEIGHT) - 1) << pos)

C=Constant()

UP=lambda pos, i:pos << i
DOWN=lambda pos,i:pos >> i
LEFT=lambda pos,i: pos >> (i * (C.HEIGHT + 1))
RIGHT=lambda pos, i: pos << (i * (C.HEIGHT + 1))
UP_LEFT=lambda pos, i: UP(LEFT(pos, i), i)
DOWN_RIGHT=lambda pos, i: DOWN(RIGHT(pos, i), i)
UP_RIGHT=lambda pos, i: UP(RIGHT(pos, i), i)
DOWN_LEFT=lambda pos, i: DOWN(LEFT(pos, i), i)
def get_winning_moves(pos, mask):
    res = UP(pos, 1) & UP(pos, 2) & UP(pos, 3)
    res |= LEFT(pos, 1) & LEFT(pos, 2) & LEFT(pos, 3)
    res |= RIGHT(pos, 1) & LEFT(pos, 1) & LEFT(pos, 2)
    res |= RIGHT(pos, 2) & RIGHT(pos, 1) & LEFT(pos, 1)
    res |= RIGHT(pos, 3) & RIGHT(pos, 2) & RIGHT(pos, 1)
    res |= UP_LEFT(pos, 1) & UP_LEFT(pos, 2) & UP_LEFT(pos, 3)
    res |= DOWN_RIGHT(pos, 1) & UP_LEFT(pos, 1) & UP_LEFT(pos, 2)
    res |= DOWN_RIGHT(pos, 2) & DOWN_RIGHT(pos, 1) & UP_LEFT(pos, 1)
    res |= DOWN_RIGHT(pos, 3) & DOWN_RIGHT(pos, 2) & DOWN_RIGHT(pos, 1)
    res |= UP_RIGHT(pos, 1) & UP_RIGHT(pos, 2) & UP_RIGHT(pos, 3)
    res |= DOWN_LEFT(pos, 1) & UP_RIGHT(pos, 1) & UP_RIGHT(pos, 2)
    res |= DOWN_LEFT(pos, 2) & DOWN_LEFT(pos, 1) & UP_RIGHT(pos, 1)
    res |= DOWN_LEFT(pos, 3) & DOWN_LEFT(pos, 2) & DOWN_LEFT(pos, 1)
    return res & (C.FULL ^ mask)



class F4State(AbNode):
    
    def __init__(self,pos=0,mask=0,moves=0,col=0) -> None:
        self.pos = pos
        self.mask = mask
        self.moves = moves
        self.col = col
        super().__init__()
        self.value = 0

    def put(self, col):
        move =  self.mask +  (1 << (col * (C.HEIGHT + 1)))
        return F4State(
            self.pos^self.mask,
            self.mask|move,
            self.moves+1,
            col        
        )
    
    def calc_value(self, *args):
        return -self.value
    
    def get_legal_moves(self):
        return (self.mask+C.BOTTOM)&C.FULL     
   
    def get_nexts(self, depth):
        if depth>4 or self.value!=0:
            return []
        leagal_move=self.get_legal_moves()
        win_state=get_winning_moves(self.pos,self.mask)
        op_win_state=get_winning_moves(self.pos^self.mask,self.mask)
        ret=[]
        for i,v in enumerate(C.CLOUMN_MASK):
            if not v&leagal_move:
                continue
            s=self.put(i)
            if v&win_state:
                s.value = 100
                return [s]
            elif v&op_win_state:
                s.value = -90
                return [s]
            ret.append(s)
        return ret 

    
    def print(self):
        # from common.util.fp import File
        ret=[]
        for i in range(C.HEIGHT-1,-1,-1):
            tmp=""
            for j in range(C.WIDTH):
                t=1<<((C.HEIGHT+1)*j+i)
                if self.mask & t:
                    if bool(self.pos&t) == bool(self.moves%2==0):
                        tmp+=" O"
                    else:
                        tmp+=" X"
                else:
                    tmp+=" -"
            ret.append(tmp)
        # File("data/log/cg/f4_grid.txt").write_file("\n".join(ret))
        return "\n".join(ret)
        #return self



class F4Serach(AlphaBateSearch):
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
            
            dict(board_rows='''11.......
11.......
11..0....
00..1....
11..00...
00..00...
101.00...'''.split('\n'),result="")
        ]
    
    def init(self,board_rows:List[str]):
        self.state=F4State()
        self.ab=F4Serach()
        ct=[[],[]]
        mv=0
        for _ in range(C.HEIGHT):
            w=board_rows.pop()
            if not w:
                continue
            for j in range(C.WIDTH):
                if w[j]=='.':
                    continue
                ct[int(w[j])].append(j)
                mv+=1
        
        for i in range(mv):
            cm=ct[i%2].pop(0)
            self.state=self.state.put(cm)
            self.log('---')
            self.log(self.state.print())    
                
    
        


    def execute(self):
        self.log(self.state.print())
        self.ab.search(self.state)
        self.log(self.state.best_action.value)
        return self.state.best_action.col


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
            self.error("--frame-flush---")
            self.init(board_rows)
            self.output(self.execute())




if __name__=='__main__':
    Solution().run()