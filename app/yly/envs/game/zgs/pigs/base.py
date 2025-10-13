from common.util.export import List, Dict, defaultdict
from ..card.export import Tao, Sha, Nzrq, Wjqf, Juedou, Wxkj, Shan, CardBase


class Pig:
    has_zg = None
    power = 4
    state = 0
    next: "Pig"
    pre: "Pig"
    IS_GOOD = 2
    IS_BAD = -2
    LIKE_BAD = -1
    UN_KNOWN = 0
    use_sha = False

    def __init__(self, idx, cards: List["CardBase"]):
        self.idx = idx
        self.cards = cards
        self.head: CardBase = CardBase()
        self.tail: CardBase = self.head
        self.card_map: Dict[str, List[CardBase]] = defaultdict(list)

    @property
    def name(self):
        return f"{self.__class__.__name__}_{self.idx}_{self.state}_{self.power}"

    @property
    def dead(self):
        return self.power == 0

    def add_card(self, c: "CardBase"):
        c.owner = self
        c.pre = self.tail
        self.tail.next = c
        self.tail = c
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

    def do(self) -> None:
        c = self.head.next
        while c:
            c.do()
            c = c.next

    def is_enemy(self, c: "Pig"):
        return False

    def is_firend(self, c: "Pig"):
        return False

    def power_change(self, num, c: "CardBase"):
        self.power += num
        from ..util import tao

        if self.power == 0:
            if tao(c.owner, self):
                self.power = 1
            else:
                self.pre.next = self.next
                self.next.pre = self.pre

    def hander(self, c: "CardBase"):
        if isinstance(c, (Nzrq, Juedou)):
            stp = Sha.type
        elif isinstance(c, (Sha, Wjqf)):
            stp = Shan.type
        if not self.card_map[stp]:
            self.power_change(-1, c)
            return False
        self.card_map[stp].pop(0).use()
        return True

    def lose_all_card(self):
        self.head.next = None
        self.has_zg = False
        self.card_map = defaultdict(list)

    def get_num_card(self, num):
        while self.cards and num > 0:
            self.add_card(self.cards.pop(0))
            num -= 1
