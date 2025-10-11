from common.mock import MockCf
from common.util.export import List, Dict, defaultdict, logger

O1 = """FP
DEAD
DEAD
J J J J J J D
"""


class CardBase:
    type: str
    is_use = False
    title = ""
    can_use = False
    pre: "CardBase" = None
    next: "CardBase" = None

    def use(self):
        logger.debug(f"use {self.title}")
        self.pre.next = self.next


class Tao(CardBase):
    type = "P"
    title = "桃"
    can_use = True


class Sha(CardBase):
    type = "K"
    title = "杀"
    can_use = True


class Shan(CardBase):
    type = "D"
    title = "闪"


class Juedou(CardBase):
    type = "F"
    title = "决"
    can_use = True


class Nzrq(CardBase):
    type = "N"
    title = "南"
    can_use = True


class Wjqf(CardBase):
    type = "W"
    title = "万"
    can_use = True


class Wxkj(CardBase):
    type = "J"
    title = "无"


class Zgll(CardBase):
    type = "Z"
    title = "诸"
    can_use = True


CARD_MAP = {s.type: s for s in CardBase.__subclasses__()}


class Pig:
    has_zg = None
    power = 4
    state = 0
    next: "Pig"
    pre: "Pig"
    IS_GOOD = 2
    IS_BAD = -2
    LIKE_GOOD = 1
    LIKE_BAD = -1

    def __init__(self, g: "Game"):
        self.g = g
        self.head: CardBase = CardBase()
        self.tail: CardBase = self.head
        self.card_map: Dict[str, List[CardBase]] = defaultdict(list)

    @property
    def dead(self):
        return self.power == 0

    def add_card(self, s: str):
        c: CardBase = CARD_MAP[s]()
        c.pre = self.tail
        self.tail.next = c
        self.tail = c
        if c.type not in self.card_map:
            self.card_map[c.type] = []
        self.card_map[c.type].append(c)
        return self

    def set_next(self, next: "Pig"):
        self.next = next
        next.pre = self

    def view(self, key="type"):
        if not self.power:
            return "DEAD"
        ret = []
        c = self.head.next
        while c:
            ret.append(getattr(c, key))
            c = c.next
        return " ".join(ret)

    def play(self):
        c = self.head.next
        while c:
            if not c.can_use:
                c = c.next
                continue
            if self.do_card(c):
                c.use()
            c = c.next

    def do_card(self, c: CardBase):
        if c.type == Tao.type and self.power < 4:
            self.power += 1
            return True
        if c.type == Zgll.type:
            self.has_zg = True
            return True
        if c.type == Wjqf.type or c.type == Nzrq.type:
            self.push_jl(c)
            return True

    def hander(self, c: CardBase):
        pass

    def hander_help(self, c: CardBase, f: "Pig"):
        if self.is_good():
            pass

    def call_help_wx(self, dst: "Pig", card: CardBase):
        p = self.next
        while p != self:
            if p.card_map[Wxkj.type]:
                if dst.state == Pig.IS_GOOD and p.state == Pig.IS_GOOD:
                    p.card_map[Wxkj.type].pop(0).use()
                    return True

            p = p.next
        return False

    def push_jl(self, c):
        p = self.next
        while p != self:
            if not self.call_help_wx(p, c):
                p.hander(c)
            p = p.next


class Mp(Pig):
    state = 2


class Zp(Pig):
    pass


class Fp(Pig):
    pass


class Game:
    mp: Mp

    def __init__(self):
        self.pigs: List[Pig] = []

    def log(self, idx):
        ret = [f"------round: {idx}------"]
        for p in self.pigs:
            if p.dead:
                continue
            ret.append(f"{p.__class__.__name__}->{p.view('title')}")
        logger.debug("\n".join(ret))


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
        self.g = Game()

        for i, hand in enumerate(hands):

            tp, *args = hand.split()
            p = mp_cls[tp](self.g)
            for a in args:
                p.add_card(a)
            if isinstance(p, Mp):
                self.g.mp = p
            if self.g.pigs:
                self.g.pigs[-1].set_next(p)
            self.g.pigs.append(p)
        p = self.g.pigs[0]
        self.g.pigs[-1].set_next(self.g.pigs[0])
        card = cards.split()
        idx = 0
        while card:
            p.add_card(card.pop(0))
            p.add_card(card.pop(0))
            self.g.log(idx)
            p.play()
            p = p.next
            idx += 1

        return self.get_result()

    def get_result(self):
        msgs = ["MP" if self.g.mp.power else "FP"]
        for p in self.g.pigs:
            msgs.append(p.view())
        return "\n".join(msgs)

    def run(self):
        n, m = self.ii()
        hands = [self.input() for _ in range(n)]
        print(self.execute(hands, self.input()))


if __name__ == "__main__":
    Solution().run()
