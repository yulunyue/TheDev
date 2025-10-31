from common.util.export import Logger, List
from .log import logger
from .util import CARD_MAP, Mp, Pig, PG_CLS, Fp


class Game:
    uri = "https://loj.ac/p/2885"

    mp: Mp

    def __init__(self):
        self.players: List[Pig] = []
        self.cards = []
        self.round = 0

    def log(self, idx):

        ret = [f"------round: {self.round}; card: {len(self.cards)}; p:{idx}------"]
        for p in self.players:
            if p.dead:
                continue
            # s={p.state}
            ret.append(f"{p.name} p={p.power}->{p.view('title')}")
        logger.debug("\n".join(ret))

    def add_pig(self, idx, tp, *cards):
        p: Pig = PG_CLS[tp](idx, self.cards)
        for c in cards:
            p.add_card(c)
        if isinstance(p, Mp):
            self.mp = p
            logger.set_mp(p)
        if isinstance(p, Fp):
            logger.fz_num_change(1)
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
        self.cards.extend(cards)

    def run(self):
        while self.cards and self.round < 3000:
            if self.mp.dead:
                break
            if logger.game_over():
                break
            self.cur_player.use_sha = False
            self.cur_player.get_num_card(2)
            self.round += 1
            self.log(self.cur_player.idx + 1)
            self.cur_player.do()
            self.cur_player = self.cur_player.next
        self.round += 1
        self.log(0)
