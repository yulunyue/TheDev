from common.mock import MockCf
from common.util.export import List, Dict, defaultdict, logger
from app.yly.envs.game.zgs.export import Game

O1 = """FP
DEAD
DEAD
J J J J J J D
"""


class Solution(MockCf):
    uri = "https://loj.ac/p/2885"

    def get_cases(self):
        return [
            dict(
                hands=["MP D D F F", "ZP N N N D", "FP J J J J"],
                cards="F F D D J J F F K D",
                result=O1,
            )
        ]

    def execute(self, hands: List[str], cards: str, **kw):
        g = Game()
        for i, hand in enumerate(hands):
            g.add_pig(i, *hand.split())
        g.load()
        card = cards.split()
        while card:
            g.add_card(card.pop(0), card.pop(0))
        return g.get_result()

    def run(self):
        n, m = self.ii()
        hands = [self.input() for _ in range(n)]
        print(self.execute(hands, self.input()))


if __name__ == "__main__":
    Solution().run()
