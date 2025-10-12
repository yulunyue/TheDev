from common.util.export import logger, List

from .util import CARD_MAP, Mp, Pig, PG_CLS


class Game:
    uri = "https://loj.ac/p/2885"

    mp: Mp

    def __init__(self):
        self.players: List[Pig] = []
        self.round = 0

    def log(self):
        ret = [f"------round: {self.round}------"]
        for p in self.players:
            if p.dead:
                continue
            ret.append(f"{p.name}->{p.view('title')}")
        logger.debug("\n".join(ret))

    def add_pig(self, idx, tp, *cards):
        p: Pig = PG_CLS[tp](idx)
        for c in cards:
            p.add_card(CARD_MAP[c]())
        if isinstance(p, Mp):
            self.mp = p
        if self.players:
            self.players[-1].set_next(p)
        self.players.append(p)

    def load(self):
        self.players[-1].set_next(self.players[0])
        self.cur_player = self.players[0]

    def add_card(self, card0, card1):
        self.cur_player.add_card(CARD_MAP[card0]())
        self.cur_player.add_card(CARD_MAP[card1]())
        self.log()
        self.cur_player.do()
        self.cur_player = self.cur_player.next
        self.round += 1

    def get_result(self):
        msgs = ["MP" if self.mp.power else "FP"]
        for p in self.players:
            msgs.append(p.view())
        return "\n".join(msgs)
