from common.util.export import List, Dict, defaultdict
from ..card.export import Tao, Sha, Nzrq, Wjqf, Juedou, Wxkj, Shan, CardBase, Zgll
from ..log import logger


class Pig:

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
        state = 1
        if self.state in {self.IS_GOOD, self.IS_BAD}:
            state = 2
        elif self.state == self.LIKE_BAD:
            state = 0
        return f"{self.__class__.__name__}_{self.idx}_{state}"

    _has_zg = False

    def haz_zg(self):
        if self.card_map[Zgll.type] and not self._has_zg:
            self.card_map[Zgll.type][0].do()
        return self._has_zg

    @property
    def dead(self):
        return self.power == 0

    def add_card(self, c: "CardBase"):
        """
        反死了，摸牌可以继续出
        """
        from ..util import CARD_MAP

        if isinstance(c, str):
            c = CARD_MAP[c]()
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
        while c and not logger.game_over():
            c.do()
            c = c.next
        """
        反死了，摸牌可以继续出
        """
        c = self.tail
        while c and not logger.game_over():
            c.do()
            c = c.next

    def is_enemy(self, c: "Pig"):
        return False

    def is_firend(self, c: "Pig"):
        return False

    def power_change(self, num, c: "CardBase"):
        # logger.debug(f"{self.name} power {self.power}->{self.power+num}")
        self.power += num

        if self.power == 0:
            logger.debug(f"{self.name} need 桃")
            s = self.card_map[Tao.type]
            if s:
                s[0].use()
                self.power = 1
            else:
                self.pre.next = self.next
                self.next.pre = self.pre

    def hander(self, c: "CardBase"):
        if c.type in {Nzrq.type, Juedou.type}:
            stp = Sha.type
        elif c.type in {Sha.type, Wjqf.type}:
            stp = Shan.type
        if not self.card_map[stp]:
            self.power_change(-1, c)
            return False
        self.card_map[stp][0].use(c)
        return True

    def lose_all_card(self):
        self.head.next = None
        self._has_zg = False
        self.card_map = defaultdict(list)

    def get_num_card(self, num):
        from ..util import CARD_MAP

        while self.cards and num > 0:
            self.add_card(self.cards[0])
            logger.debug(f"{self.name} get {CARD_MAP[self.cards[0]].title}")
            num -= 1
            if len(self.cards) > 1:
                self.cards.pop(0)
