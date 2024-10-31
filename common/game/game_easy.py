from .game_base import GameBase, PlayerBase, Node
from common.algo.absearch import AlphaBateSearchDev
import sys


class GameNumChoice(GameBase):
    '''
                                           a:4
                                           min                                
          b:2                  c:6                    d:3             e:2            
          max                  max                    max
    f:8   g:2   h:7       i:1  j:4?  k:2?      l:3    m:6   n:9
    min
o:8     p:9                                                 
    '''
    name = "GameNumChoice"
    tree_map = '''
a: 4
  b:
    f:
      o: 8
      p: 9
    g: 2
    h: 7
  c:
    i: 1
    j: 1
    k: 4
  d:
    l: 3
    m: 6
    n: 9
  e: 2
'''

    def init(self):
        self.env = Node().load_from_yml(self.tree_map)
        self.set_player([
            AlphaBateSearchDev('p1'),
            AlphaBateSearchDev('p2')
        ])

    def get_game_round(self):
        return 1


if __name__ == '__main__':
    GameNumChoice().run()
