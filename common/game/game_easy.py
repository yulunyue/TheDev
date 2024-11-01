from .game_base import GameBase, PlayerBase
from common.algo.absearch import AlphaBateSearchDev, AbNode
import sys


class GameNumChoice(GameBase):
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
        self.env = AbNode("").load_from_yml(self.tree_map)
        self.set_player([
            AlphaBateSearchDev('p1'),
            AlphaBateSearchDev('p2')
        ])

    def get_game_round(self):
        return 1


if __name__ == '__main__':
    GameNumChoice().run()
