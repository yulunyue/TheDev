from common.util.export import logger


class CardBase:
    type: str
    is_use = False
    title = ""
    pre: "CardBase" = None
    next: "CardBase" = None

    def set_owner(self, owner):
        from ..pigs.base import Pig

        self.owner: Pig = owner

    def use(self):
        logger.debug(f"{self.owner.name} use {self.title}")
        self.pre.next = self.next
        if self.next:
            self.next.pre = self.pre
        else:
            self.owner.tail = self.pre

    def do(self, f: "CardBase" = None):
        self.use()

    def wx(self, t):
        dst = self.owner.next
        from .wxkj import Wxkj

        while dst != self.owner:
            wx = dst.card_map[Wxkj.type]
            if not wx:
                dst = dst.next
                continue
            if dst.is_firend(t) or dst.is_enemy(self.owner):
                dst.card_map[Wxkj.type].pop(0).use()
                return True
            dst = dst.next
        return False
