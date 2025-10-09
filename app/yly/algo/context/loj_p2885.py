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
    桃: CardBase = C("P")
    杀: CardBase = C("K")
    闪: CardBase = C("D")
    决斗: CardBase = C("F")
    南猪入侵: CardBase = C("N")
    万箭齐发: CardBase = C("W")
    无懈可击: CardBase = C("J")
    猪哥连弩: CardBase = C("Z")


class Pig:
    猪哥连弩 = None
    power = 4

    def __init__(self, g: "Game"):
        self.g = g
        self.pos_idx = len(g.pigs)
        g.pigs.append(self)

    @property
    def dead(self):
        return self.power == 0

    def set_cards(self, cards):
        self.cards: List[CardBase] = []
        self.card_map: Dict[str, List[CardBase]] = dict()
        for c in cards:
            self.add(c)
        return self

    def add(self, s: str):
        c: CardBase = CARD_MAP[s]()
        self.cards.append(c)
        if c.type not in self.card_map:
            self.card_map[c.type] = []
        self.card_map[c.type].append(c)
        return self

    def get_nexts(self):
        ret: List[Pig] = []
        nid = (self.pos_idx + 1) % len(self.g.pigs)
        while nid != self.pos_idx:
            n = self.g.pigs[nid]
            nid = (nid + 1) % len(self.g.pigs)
            if n.dead:
                continue
            ret.append(n)
        return ret

    def view(self):
        if not self.power:
            return "DEAD"
        return " ".join([c.type for c in self.cards if not c.is_use])

    def play(self):
        while self.power < 4 and self.card_map[CT.桃.type]:
            self.power += 1
            c = self.card_map[CT.桃.type].pop()
            c.is_use = True
        for tp in [CT.猪哥连弩.type, CT.万箭齐发.type, CT.南猪入侵.type]:
            while self.card_map.get(tp):
                c = self.card_map[tp].pop()
                if tp == CT.猪哥连弩.type:
                    self.猪哥连弩 = c
                else:
                    for next_pid in self.get_nexts():
                        next_pid.hander(c)
                c.is_use = True

    def hander(self, c: CardBase):
        if c == CT.南猪入侵.type:
            pass
        elif c == CT.万箭齐发.type:
            pass


class Mp(Pig):
    pass


class Zp(Pig):
    pass


class Fp(Pig):
    pass


class Game:
    def __init__(self):
        self.pigs: List[Pig] = []

    def add_pig(self, p: Pig):
        if isinstance(p, Mp):
            self.zp = p


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

        mp_cls = dict(MP=Mp, ZP=Zp, FP=Fp)
        g = Game()
        for hand in hands:
            tp, *args = hand.split()
            p = mp_cls[tp](g).set_cards(args)
            g.add_pig(p)

        card = cards.split()
        p = g.zp
        while card and not p.dead:
            p.add(card.pop(0))
            p.add(card.pop(0))
            p.play()
            p = p.get_nexts()[0]
        msgs = ["MP" if g.zp.power else "FP"]
        for p in g.pigs:
            msgs.append(p.view())
        return "\n".join(msgs)

    def run(self):
        n, m = self.ii()
        hands = [self.input() for _ in range(n)]
        print(self.execute(hands, self.input()))


if __name__ == "__main__":
    Solution().run()
