from .base import CardBase


class Juedou(CardBase):
    type = "F"
    title = "决"
    can_use = True

    def do(self, f: CardBase = None):
        from ..util import wx

        cur = self.owner.next
        while cur != self.owner:
            if self.owner.is_enemy(cur):
                self.use()
                if not wx(self.owner, cur, self.owner.IS_BAD):
                    cur.hander(self)
                    return
            cur = cur.next
