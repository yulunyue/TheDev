from common.util.export import logger, List

from .util import CARD_MAP, Mp, Pig, PG_CLS


class Game:
    uri = "https://loj.ac/p/2885"

    mp: Mp

    def __init__(self):
        self.players: List[Pig] = []
        self.cards = []
        self.round = 0

    def log(self):
        ret = [f"------round: {self.round}------"]
        for p in self.players:
            if p.dead:
                continue
            ret.append(f"{p.name}->{p.view('title')}")
        logger.debug("\n".join(ret))

    def add_pig(self, idx, tp, *cards):
        p: Pig = PG_CLS[tp](idx, self.cards)
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

    def get_result(self):
        msgs = ["MP" if self.mp.power else "FP"]
        for p in self.players:
            msgs.append(p.view())
        return "\n".join(msgs)

    def set_cards(self, cards):
        self.cards.extend([CARD_MAP[c]() for c in cards])

    def run(self):
        self.round += 1
        while self.cards:
            self.cur_player.use_sha = False
            self.cur_player.get_num_card(2)
            self.log()
            self.cur_player.do()
            if self.mp.dead:
                break
            self.cur_player = self.cur_player.next
            self.round += 1
