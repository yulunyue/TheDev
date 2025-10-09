from common.mock import MockCf
from common.util.export import List, Dict

O1 = """FP
DEAD
DEAD
J J J J J J D
"""


class CardBase:
    type: str
    is_use = False


CARD_MAP = dict()


def C(k):
    class Card(CardBase):
        type = k

    CARD_MAP[k] = Card
    return CARD_MAP[k]


class CT:
    桃 = C("P")
    杀 = C("K")
    闪 = C("D")
    决斗 = C("F")
    南猪入侵 = C("N")
    万箭齐发 = C("W")
    无懈可击 = C("J")
    猪哥连弩 = C("Z")


class Pig:
    猪哥连弩 = None
    power = 4

    def __init__(self, pos_idx):
        self.pos_idx = pos_idx

    def set_cards(self, cards):
        self.cards: List[CardBase] = []
        self.card_map: Dict[str, List[CardBase]] = dict()
        for c in cards:
            self.add(c)
        return self

    def add(self, s: str):
        c: CardBase = CARD_MAP[s]()
        if isinstance(c, CT.猪哥连弩):
            self.猪哥连弩 = c
        self.cards.append(c)
        if c.type not in self.card_map:
            self.card_map[c.type] = []
        self.card_map[c.type].append(c)
        return self


class Mp(Pig):
    pass


class Zp(Pig):
    pass


class Fp(Pig):
    pass


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

    zp: Zp

    def execute(self, hands: List[str], cards: str, **kw):
        self.pigs: List[Pig] = []
        mp_cls = dict(MP=Mp, ZP=Zp, FP=Fp)

        Solution.msgs = []
        for hand in hands:
            tp, *args = hand.split()
            p = mp_cls[tp](len(self.pigs)).set_cards(args)
            if isinstance(p, Zp):
                self.zp = p
            self.pigs.append(p)
        card = cards.split()
        for i in range(0, len(card), 2):
            p = self.pigs[i % len(self.pigs)]
            p.add(card[i])
            p.add(card[i + 1])

        return "\n".join(Solution.msgs)

    def run(self):
        n, m = self.ii()
        hands = [self.input() for _ in range(n)]
        print(self.execute(hands, self.input()))


if __name__ == "__main__":
    Solution().run()
