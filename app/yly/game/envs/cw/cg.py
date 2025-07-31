from app.yly.game.envs.cw.model.world import World, C
from common.mock import MockCg

from common.algo.search.alphabate_search import AlphaBateSearch


class CgCw(MockCg):
    """
    https://www.codingame.com/ide/puzzle/cultist-wars
    """

    name = "cw"
    game_id = "72806721d45bcc88f2891a7927b73fbfa911b50b"
    agentsIds = [-1, -2]

    def get_player(self):
        return AlphaBateSearch().load(1)

    def main(self):
        algo = self.get_player()
        player_id = self.ii()[0]
        # 0 - you are the first player, 1 - you are the second player
        # width: Width of the board
        # height: Height of the board
        _, height = self.ii()
        maps = []

        for _ in range(height):
            maps.append(self.input())
        w = World(",".join(maps), player_id)
        # game loop
        while True:
            num_of_units = int(input())  # The total number of units on the board
            shapes = []
            for _ in range(num_of_units):
                # unit_id: The unit's ID
                # unit_type: The unit's type: 0 = Cultist, 1 = Cult Leader
                # hp: Health points of the unit
                # x: X coordinate of the unit
                # y: Y coordinate of the unit
                # owner: id of owner player
                shapes.append(self.input())
            w.set_shapes(",".join(shapes))

            # Write an action using print
            self.log(**w.to_json())

            # WAIT | unitId MOVE x y | unitId SHOOT target| unitId CONVERT target
            self.output("WAIT")


if __name__ == "__main__":
    CgCw().main()
