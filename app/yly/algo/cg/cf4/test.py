from common.util.test import TestBase, logger
from app.yly.algo.cg.cf4.env import Env, PLAYERS, S, get_player, Algo, SE, C
from app.yly.algo.cg.cf4.states.c4_grid_state import C4GridState
from common.algo.search.algo import random_seed
from typing import List


class C4Test(TestBase):
    def __init__(self):
        super().__init__()

    def get_env(self, debug=1):

        return Env(
            debug=debug,
            width=7,
            height=6,
            # env_name=Env.connectx,
        )

    def test_init(self):

        C.load(6, 7)
        w1, h1 = C.WIDTH - C.inarow + 1, C.HEIGHT - C.inarow + 1
        SIZE = C.WIDTH * C.HEIGHT
        self.expect(
            len(C.lines),
            C.WIDTH * h1 + C.HEIGHT * w1 + 2 * w1 * h1,
        )
        self.expect(
            C.lines[:4],
            [
                [[0, 0, 0, 0], [0, 1, 1, 0], [0, 2, 2, 0], [0, 3, 3, 0]],
                [[0, 0, 0, 1], [1, 0, 1, 1], [2, 0, 2, 1], [3, 0, 3, 1]],
                [[0, 0, 0, 2], [1, 1, 1, 2], [2, 2, 2, 2], [3, 3, 3, 2]],
                [[0, 1, 0, 3], [0, 2, 1, 3], [0, 3, 2, 3], [0, 4, 3, 3]],
            ],
        )
        self.expect(C.point_line_id[0], [[0, 0, 0], [1, 1, 0], [2, 2, 0]])
        self.expect(
            C.point_line_id[7 * 6 // 2],
            [[1, 1, 3], [16, 1, 2], [31, 1, 1], [45, 0, 0], [46, 3, 0]],
        )

        grid_state = C4GridState().init_root()
        action = grid_state.get_action(0).dst.get_action(0).dst
        # self.expect(action.line_state, [1])
        grids = action.get_grid()
        self.expect(len(grids), SIZE)
        self.expect(grids[-C.WIDTH], 1)
        self.expect(grids[-2 * C.WIDTH], 2, grids)

    def test_player_all(self):
        env = self.get_env()
        for k in PLAYERS:
            action = env.play(get_player(k))
            logger.info(k)
            logger.info(action)

    def test_player_kd1(self):
        logger.info(self.get_env().play(get_player("kd1")))

    def test_action(self):
        a = self.get_action().dst.get_action(0)
        a = a.dst.get_action(0)
        self.expect(a.get_points(), [0, 0, 0, 0, 0, 1], a)

    def test_pk(self):
        players = [get_player("ab1"), get_player("ab5")]
        for _ in range(2):
            env = self.get_env()  # , env_name=Env.connectx)
            # Play as the first agent against "negamax" agent.
            result = env.run(players)
            env.render(mode="html", width=500, height=450)
            if result is None:
                logger.info(f"unknow error")
            elif result >= 0:
                logger.info(f"[{players[result].name}][{S[result]}] win")
            else:
                logger.info("no win")
            players.reverse()

    def test_fight(self):
        """
        所有玩家一起战斗看看谁是第一名
        """

        players = [get_player(k) for k in PLAYERS]
        fight_result = {
            v.name: dict(win=0, draw=0, lose=0, use_time=0, max_time=0) for v in players
        }

        def update(state: int, players: List[Algo]):
            if state is None:
                logger.info(f"unknow state {state} {players[0].name} {players[1].name}")
                return
            if state == -1:
                fight_result[players[0].name]["draw"] += 1
                fight_result[players[1].name]["draw"] += 1
                info = "DRAW"
            else:
                w, l = players[state].name, players[1 - state].name
                fight_result[w]["win"] += 1
                fight_result[l]["lose"] += 1
                info = f"WIN->{w}{S[state]} LOSE->{l}{S[1 - state]} "
            logger.info(f"{players[0].name} pk {players[1].name} {info}")
            for p in players:
                fight_result[p.name]["use_time"] += p.use_time
                fight_result[p.name]["max_time"] = max(
                    fight_result[p.name]["max_time"], p.max_use_time
                )

        for pk_num in range(1):
            for i in range(len(players)):
                for j in range(i + 1, len(players)):
                    ps = [players[i], players[j]]
                    update(self.get_env().run(ps), ps)
                    ps.reverse()
                    update(self.get_env().run(ps), ps)
        logger.table(fight_result, lambda a: [a["win"], a["draw"], a["lose"]])


if __name__ == "__main__":
    random_seed()
    C4Test().run()
