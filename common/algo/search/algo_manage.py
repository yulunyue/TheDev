from common.algo.search.algo import Algo
from common.algo.search.state import State, Action
from common.util.export import logger, File, List, defaultdict


class ALgoManage:
    record_dir = ""

    def set_players(self, players: List[Algo]):
        self.players: List[Algo] = players
        self.fight_result = defaultdict(
            lambda: dict(WIN=0, LOSE=0, DRAW=0, use_time=0, max_time=0)
        )
        return self

    def set_state(self, state):
        self.state: State = state
        return self

    def get_state(self, idx, dst=None) -> State:
        if callable(self.state):
            return self.state(idx, dst)
        return dst

    def fight(self, pk_round=1):
        for _ in range(pk_round):
            for i in range(len(self.players)):
                for j in range(len(self.players)):
                    if i != j:
                        self.pk([self.players[i], self.players[j]])
                    self.pk([self.players[j], self.players[i]])
        logger.table(self.fight_result, lambda a: [a["WIN"], a["DRAW"], a["DRAW"]])
        return self.fight_result

    def pk(self, players1: List[Algo]):
        win_idx: int = self.actor(players1)
        s = f"{players1[0].get_name()} pk {players1[1].get_name()} "
        keys = [f"{players1[i].get_name()}_{i}" for i in range(len(players1))]
        if 0 <= win_idx < len(players1):
            self.fight_result[keys[win_idx]]["LOSE"] += 1
            self.fight_result[keys[1 - win_idx]]["WIN"] += 1
            s += f"[{keys[win_idx]}][LOSE]"
        else:
            self.fight_result[keys[0]]["DRAW"] += 1
            self.fight_result[keys[1]]["DRAW"] += 1
            s += f"[DRAW]"
        logger.info(s)
        return self

    def actor(self, players: List[Algo], max_turn=5000):
        """
        返还输的玩家ID
        """

        player_idx = 0
        self.turn_idx = 0
        s = self.get_state(0, self.state).reset_env()
        self.rewards = [[0] * len(players)]
        while True:
            if s.get_done():
                self.record(players, None, player_idx, s)
                break
            a = players[player_idx].search(s)
            if a is None:
                self.record(players, a, player_idx, s)
                return s.get_win_player(self.rewards, (player_idx + 1) % len(players))
            self.record(players, a, player_idx, s)
            player_idx = (player_idx + 1) % len(players)
            self.turn_idx += 1
            if self.turn_idx >= max_turn:
                break
            s = self.get_state(self.turn_idx, a.dst)
        # if s:
        #     self.record(players, s)
        return s.get_win_player(self.rewards, player_idx)

    def set_record_dir(self, path: str):
        self.record_dir = path
        return self

    def record(self, players: List[Algo], a: Action, player_idx, s: State):
        if not self.record_dir:
            return
        self.rewards.append(self.rewards[-1].copy())
        reward = 0
        if a is not None:
            reward = a.get_reward()
        self.rewards[-1][player_idx] += reward
        info = players[player_idx].name
        if reward > 0:
            info += f" WIN {reward}"
        elif reward < 0:
            info += f" LOS {reward}"
        msg = f"{s}\nturn: {self.turn_idx}; reward_all: {self.rewards[-1]}; info: {info}\n"
        file_name = "_pk_".join([v.get_name() for v in players])
        file_path = f"{self.record_dir}/{file_name}.log"
        fp = File(file_path).get_writer()
        fp.write(msg)
        fp.flush()

    def train(self, players: List[Algo], epochs=1):
        win_count = defaultdict(int)
        for _ in range(epochs):
            win_idx = self.actor(players)
            win_count[win_idx] += 1
        return win_count
