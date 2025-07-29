from app.yly.game.envs.cw.model.world import World, C
from common.mock import MockCg


class CgCw(MockCg):
    """
    https://www.codingame.com/ide/puzzle/cultist-wars
    """

    name = "cw"
    game_id = "72806721d45bcc88f2891a7927b73fbfa911b50b"
    agentsIds = [-1, -2]

    def main(self):

        player_id, *args = (
            self.ii()
        )  # 0 - you are the first player, 1 - you are the second player
        # width: Width of the board
        # height: Height of the board
        width, height = self.ii()
        maps = []

        for i in range(height):
            maps.append(self.input())
        w = World().load(width=width, height=height, maps=maps).set_player_id(player_id)
        # game loop
        while True:
            num_of_units = int(input())  # The total number of units on the board
            shapes = []
            for i in range(num_of_units):
                # unit_id: The unit's ID
                # unit_type: The unit's type: 0 = Cultist, 1 = Cult Leader
                # hp: Health points of the unit
                # x: X coordinate of the unit
                # y: Y coordinate of the unit
                # owner: id of owner player
                shapes.append(self.ii())
            w.set_shapes(shapes)

            # Write an action using print
            self.log(**w.to_json())

            # WAIT | unitId MOVE x y | unitId SHOOT target| unitId CONVERT target
            self.output(w.get_action()[1])


if __name__ == "__main__":
    CgCw().main()
