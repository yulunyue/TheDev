from app.yly.algo.manage import SolutionBase,View
from common.algo.absearch import AlphaBateSearch,AbNode
from typing import Dict,List
from functools import lru_cache
MOD=(10**9)+7
inf = float("inf")
HEIGHT=7
WIDTH=9
FOUR=4
class G4:
    def __init__(self):
        self.grid=[for _ in range()]
    def put():
        pass

g4=G4()

class F4State(AbNode):
    pass

class F4Serach(AlphaBateSearch):
    pass

class Solution(SolutionBase):
    uri="https://www.codingame.com/ide/puzzle/connect-4"
    game_id = '70989246b492bcc523436cf43b6090c82395d392'
    agentsIds = [
        -1, -2
    ]
    def get_cases(self):
        return [
            dict(board_rows=[],result="")
        ]
    
    def init(self,board_rows):
        self.board_rows=board_rows
        for i,w in self.board_rows[::-1]:
            pass
        return self.execute()
    def execute(self):
        pass
    def exec(self):
        my_id, opp_id = [int(i) for i in input().split()]
        # game loop
        while True:
            turn_index = int(input())  # starts from 0; As the game progresses, first player gets [0,2,4,...] and second player gets [1,3,5,...]
            board_rows=[]
            for i in range(7):
                board_rows.append(input())  # one row of the board (from top to bottom)
            num_valid_actions = int(input())  # number of unfilled columns in the board
            for i in range(num_valid_actions):
                action = int(input())  # a valid column index into which a chip can be dropped
            opp_previous_action = int(input())  # opponent's previous chosen column index (will be -1 for first player in the first turn)
            self.init(board_rows)
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr, flush=True)


            # Output a column index to drop the chip in. Append message to show in the viewer.
            print(self.execute())




if __name__=='__main__':
    Solution().run()