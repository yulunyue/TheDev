"""
https://www.codingame.com/ide/puzzle/cultist-wars
"""

from common.third_util.cg_util import CodingGame
from .world import World
import sys
import math


class CgCw(CodingGame):

    def run(self):

        my_id = int(
            input()
        )  # 0 - you are the first player, 1 - you are the second player
        # width: Width of the board
        # height: Height of the board
        width, height = [int(i) for i in input().split()]
        for i in range(height):
            y = input()  # A y of the board: "." is empty, "x" is obstacle

        # game loop
        while True:
            num_of_units = int(input())  # The total number of units on the board
            for i in range(num_of_units):
                # unit_id: The unit's ID
                # unit_type: The unit's type: 0 = Cultist, 1 = Cult Leader
                # hp: Health points of the unit
                # x: X coordinate of the unit
                # y: Y coordinate of the unit
                # owner: id of owner player
                unit_id, unit_type, hp, x, y, owner = [int(j) for j in input().split()]

            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr, flush=True)

            # WAIT | unitId MOVE x y | unitId SHOOT target| unitId CONVERT target
            print("WAIT")


if __name__ == "__main__":
    CgCw().run()
