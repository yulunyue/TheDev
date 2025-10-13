from common.mock import MockCf
from common.util.export import List, Dict, defaultdict, logger
from app.yly.envs.game.zgs.export import Game

O1 = """FP
DEAD
DEAD
J J J J J J D"""
O2 = """MP
P

N N J N J
DEAD
D P
DEAD
Z W
DEAD
DEAD
DEAD"""


class Solution(MockCf):
    uri = "https://loj.ac/p/2885"

    def get_cases(self):
        return [
            # dict(
            #     hands=["MP D D F F", "ZP N N N D", "FP J J J J"],
            #     cards="F F D D J J F F K D",
            #     result=O1,
            # ),
            dict(
                hands=[
                    "MP J P J Z",
                    "ZP J J N J",
                    "ZP F N N P",
                    "ZP F W J Z",
                    "ZP P D D P",
                    "ZP F W J W",
                    "ZP K Z P W",
                    "FP J J J J",
                    "FP J J K J",
                    "FP J J Z J",
                ],
                cards="Z N J K Z",
                result=O2,
            ),
        ]

    def execute(self, hands: List[str], cards: str, **kw):
        g = Game()
        for i, hand in enumerate(hands):
            g.add_pig(i, *hand.split())
        g.load()
        g.set_cards(cards.split())
        g.run()
        return g.get_result()

    def run(self):
        n, m = self.ii()
        hands = [self.input() for _ in range(n)]
        print(self.execute(hands, self.input()))


if __name__ == "__main__":
    Solution().run()
