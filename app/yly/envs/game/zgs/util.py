from .card.export import Tao, Sha, Nzrq, Wjqf, Juedou, Wxkj, Shan, CardBase, Zgll
from .pigs.fp import Fp
from .pigs.zp import Zp
from .pigs.mp import Mp
from .pigs.base import Pig, logger

CARD_MAP = {s.type: s for s in [Tao, Sha, Nzrq, Wjqf, Juedou, Wxkj, Shan, Zgll]}
PG_CLS = dict(MP=Mp, ZP=Zp, FP=Fp)


def wx(c: Pig, t: Pig, tp, card: CardBase):
    cur = c
    while True:
        s = cur.card_map[Wxkj.type]
        if s and tp == Pig.IS_GOOD and cur.is_enemy(t):
            c1 = s[0].use(card)
            return not wx(cur, t, -tp, c1)
        if s and tp == Pig.IS_BAD and cur.is_firend(t):
            c1 = s[0].use(card)
            return not wx(cur, t, -tp, c1)
        cur = cur.next
        if cur == c:
            break
    return False
