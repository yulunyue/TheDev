from common.util.export import logger
from common.mock import MockCg
from app.yly.game.envs.kululu.model.grid import Grid


class Kululu(MockCg):
    name = "kululu"
    uri = "https://www.codingame.com/ide/puzzle/code-of-kutulu"
    game_id = "59755350863a5f654a8f27dc827b976824254c5b"
    agentsIds = [-1, 5751943, 3995777, 4762568]

    def main(self):
        self.input()
        h = int(self.input())
        g = Grid()
        g.load_map([self.input() for _ in range(h)])

        # sanity_loss_lonely: how much sanity you lose every turn when alone, always 3 until wood 1
        # sanity_loss_group: how much sanity you lose every turn when near another player, always 1 until wood 1
        # wanderer_spawn_time: how many turns the wanderer take to spawn, always 3 until wood 1
        # wanderer_life_time: how many turns the wanderer is on map after spawning, always 40 until wood 1
        g.load_param(self.ii())
        # game loop
        while True:
            entity_count, *args = self.ii()
            players = []
            for _ in range(entity_count):
                players.append(self.input().split())
            g.set_players(players)

            self.log(**g.dump())
            # info = g.get_action()
            # if info:
            #     self.output(f"MOVE {info[1]} {info[0]}")
            # else:
            self.output("WAIT")


if __name__ == "__main__":
    Kululu().main()
