from .card.export import Tao, Sha, Nzrq, Wjqf, Juedou, Wxkj, Shan, CardBase
from .pigs.fp import Fp
from .pigs.zp import Zp
from .pigs.mp import Mp
from .pigs.base import Pig

CARD_MAP = {s.type: s for s in [Tao, Sha, Nzrq, Wjqf, Juedou, Wxkj, Shan]}
PG_CLS = dict(MP=Mp, ZP=Zp, FP=Fp)


def wx(c: Pig, t: Pig, tp):
    cur = c.next
    while cur != c:
        s = cur.card_map[Wxkj.type]
        if not s:
            cur = cur.next
            continue
        if tp == Pig.IS_GOOD and cur.is_enemy(t):
            s.pop(0).use()
            return not wx(cur, t, -tp)
        if tp == Pig.IS_BAD and cur.is_firend(t):
            s.pop(0).use()
            return not wx(cur, t, -tp)
        cur = cur.next
    return False


def tao(c: Pig, t: Pig):
    cur = c
    while cur != c:
        s = cur.card_map[Tao.type]
        if s and cur.is_firend(t):
            s.pop(0).use()
            return True
        cur = cur.next
    return False
