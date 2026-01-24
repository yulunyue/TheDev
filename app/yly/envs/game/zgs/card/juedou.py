from .base import CardBase, logger, List


class Juedou(CardBase):
    type = "F"
    title = "决"

    def do(self):
        from ..util import wx, Fp

        aim = None
        if self.owner.__class__ == Fp:
            aim = logger.mp
            self.owner.is_enemy(aim)
        else:
            cur = self.owner.next
            while cur != self.owner:
                if self.owner.is_enemy(cur):
                    aim = cur
                    break
                cur = cur.next
        if aim is not None:
            self.use()
            if not wx(self.owner, aim, self.owner.IS_BAD, self):
                handers: List[Fp] = [aim, self.owner]
                idx = 0
                while handers[idx].hander(self):
                    self.set_owner(handers[idx])
                    idx = (idx + 1) % 2
