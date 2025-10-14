from .base import CardBase


class Sha(CardBase):
    type = "K"
    title = "杀"

    def do(self, f=None):
        if not self.owner.has_zg and self.owner.use_sha:
            return
        if self.owner.is_enemy(self.owner.next):
            self.set_dst(self.owner.next)
            super().do(f)
            self.owner.use_sha = True
            self.owner.next.hander(self)
