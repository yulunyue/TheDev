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
