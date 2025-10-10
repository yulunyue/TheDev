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

    def is_gl(self):
        return self.type in {
            CT.南猪入侵.type,
            CT.万箭齐发.type,
            CT.决斗.type,
            CT.无懈可击.type,
        }


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
    state = 0

    def __init__(self, g: "Game"):
        self.g = g
        self.pos_idx = len(g.pigs)
        g.pigs.append(self)

    @property
    def is_good(self):
        return self.state == 2

    @property
    def is_bad(self):
        return self.state == -2

    @property
    def like_good(self):
        return self.state == 1

    @property
    def like_bad(self):
        return self.state == -1

    @property
    def is_unknow(self):
        return self.state == 0

    @property
    def dead(self):
        return self.power == 0

    def set_cards(self, cards):
        self.cards: List[CardBase] = []
        self.can_use_cards: List[CardBase] = []
        self.card_map: Dict[str, List[CardBase]] = dict()
        for c in cards:
            self.add(c)
        return self

    def add(self, s: str):
        c: CardBase = CARD_MAP[s]()
        self.cards.append(c)
        self.can_use_cards.append(c)
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
        i = 0
        while i < len(self.can_use_cards):
            c = self.can_use_cards[i]
            if c.is_use:
                self.can_use_cards.pop(i)
                continue
            if self.do_card(c):
                c = self.can_use_cards.pop(i)
                c.is_use = True
                continue
            i += 1

    def do_card(self, c: CardBase):
        if c.type == CT.桃.type and self.power < 4:
            self.power += 1
            return True
        if c.type == CT.猪哥连弩.type:
            self.猪哥连弩 = c
            return True
        if c.type == CT.万箭齐发.type or c.type == CT.南猪入侵.type:
            self.push(c)
            return True
        if c.type == CT.决斗.type:
            return self.juedo(c)
        return False

    def hander(self, c: CardBase):
        if c.is_gl() and self.call_help(c):
            pass

    def hander_help(self, c: CardBase, f: "Pig"):
        if self.is_good():
            pass

    def call_help(self, c: CardBase):
        for d in self.get_nexts():
            if d.hander_help(c, self):
                return True

    def push(self, c):
        for d in self.get_nexts():
            d.hander(c)

    def juedo(self, c: CardBase):
        pass


class Mp(Pig):
    state = 2


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
