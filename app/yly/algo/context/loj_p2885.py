from common.mock import MockCf
from common.util.export import List, Dict, defaultdict, logger
from app.yly.envs.game.zgs.export import Game, logger


class Solution(MockCf):
    uri = "https://loj.ac/p/2885"

    def set_logger(self, log):
        logger.logger = log

    def do(self, hands: List[str], cards: str, **kw):
        g = Game()
        for i, hand in enumerate(hands):
            g.add_pig(i, *hand.split())
        g.load()
        g.set_cards(cards.split())
        g.run()
        return g.get_result()

    def execute(self):
        n, m = self.ii()
        hands = [self.input() for _ in range(n)]
        return self.do(hands, self.input())


if __name__ == "__main__":
    print(Solution().execute())
