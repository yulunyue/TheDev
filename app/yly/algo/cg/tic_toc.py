from collections import defaultdict
from common.algo.absearch import AlphaBateSearch,AbNode,inf
from app.yly.algo.manage import SolutionBase
from typing import List,Dict
POS = [4, 1, 3, 5, 7, 0, 2, 6, 8]
POS_LINE=[[] for _ in range(len(POS))]
LINES = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
SCORE_MAP=dict()
def get_score(a,b,c,v):
    s1=a*9+b*3+c
    SCORE_MAP[s1]=v
    def u(g):
        return 2 if g==1 else 0
    d,e,f=u(a),u(b),u(c)
    s2=d*9+e*3+f
    SCORE_MAP[s2]=-v
    return [s1,s2]

WIN = get_score(1,1,1,100)

def init():
    for i,l in enumerate(LINES):
        for j,v in enumerate(l):
            POS_LINE[v].append([i,j])
init()
class Grid3:
    def init(self):
        super().init()
        self.grid=[0]*9
        self.lines=[0 for _ in range(len(LINES))]
        self.state_ct=defaultdict(int)
        self.state[0]=len(LINES)
        self.state=0
    
    def put3(self, pos, val):
        self.grid[pos]=val
        for i,j in POS_LINE[pos]:
            self.lines[i][j]=val
            state=self.lines[i][0]*9+self.lines[i][1]*3+self.lines[i][1]
            self.set_state(i,state)
        if self.state_ct[WIN[0]]:
            return 1
        if self.state_ct[WIN[1]]:
            return 2
        return 0
    
    def set_state(self,i,state):
        self.state_ct[self.lines[i]]-=1
        self.state[state]+=1
        self.lines[i] = state
        
    def get_moves(self):
        return [p for p in POS if self.grid[p]==0]

class Grid9(Grid3):
    def init(self):
        super().init()
        self.grid:List[Grid3]=[Grid3() for _ in range(9)]

    def put(self, i:int, j:int, op):
        self.i,self.j=i,j
        op=self.grid[self.i].put3(self.j, op)

    def get_score(self, depth):
        return self.score if self.play_id == 1 else -self.score


    
G=Grid9()
class Move(AbNode):
    def __init__(self,y,x) -> None:
        self.y=y
        self.x=x
    
    def do(self,op):
        self.op=op
        if G.grid[self.y].grid[self.x]==op:
            return self
        G.put(self.y,self.x,op)
        return self
    
    def get_nexts(self, depth):
        ret:List[Move]=[]
        for p in POS:
            if G.grid[p].state:
                pass
            ret = self.nodes[last_move[1]].get_moves(self.play_id)
        else:
            ret = []
            for n in self.nodes_sort:
                if n.win_state:
                    continue
                ret.extend(n.get_moves(self.play_id))
        # ret = sorted(ret, key=lambda v: v[2],
        #              reverse=True if op == 1 else False)[:7]
        return ret


PLAYER_OP=0
PLAYER_SELF=1


class Solution(SolutionBase):
    uri = "https://www.codingame.com/ide/puzzle/tic-tac-toe"
    gameid = '6246186678d52f83e9a2d47885d4b6f60900eed7'
    game_type = 'pk'
    name = "tic_toc"
    agentsIds = [
        # 5604295,
        -2, -1
    ]
    _has_view = True
    def __init__(self) -> None:
        self.search = AlphaBateSearch()
        self.mvs:List[Move] = []

    def get_cases(self):
        return [
            dict(opponent_row=[],opponent_col=[],row=[],col=[],result=""),
            # dict(result="0 1", pre=[]),
        ]

    def init(self,opponent_row,opponent_col,row,col,**kw):
        if opponent_row != -1 and  opponent_col == -1:
            self.mvs.append(Move(opponent_row,opponent_col).do(PLAYER_OP))
     

    def execute(self):
        if self.mvs:
            self.mvs.append(self.search.search(self.mvs[-1], 4))
        else:
            self.mvs.append(Move(4,4))
        self.mvs[-1].do(PLAYER_SELF)
        return f'{self.mvs[-1].y} {self.mvs[-1].x}'


    def exec(self):
        while True:
            opponent_row, opponent_col = [int(i) for i in input().split()]
            valid_action_count = int(input())
            for i in range(valid_action_count):
                row, col = [int(j) for j in input().split()]
            self.init(opponent_row,opponent_col,row,col)
            self.output(self.execute())

if __name__ == '__main__':
    Solution().run()
