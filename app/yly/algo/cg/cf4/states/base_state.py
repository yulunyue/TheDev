from typing import Dict, List
from common.algo.search.state import State, Action, inf
from app.yly.algo.cg.cf4.constant import C, S


class F4State(State):

    def __init__(self):
        super().__init__(0, 0)

    def get_grid(self):
        pass

    def get_mask(self):
        grid = self.get_grid()
        return C.grid_to_mask(grid)

    def to_str(self):
        return (
            "\n"
            + "\n".join(
                [
                    f"done:{self.done},depth:{self.depth}",
                    f"mask:{self.get_mask()}",
                    C.grid_view(self.get_grid()),
                ]
            )
            + "\n"
        )

    def __str__(self):
        return self.to_str()
