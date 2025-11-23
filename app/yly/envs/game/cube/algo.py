from common.algo.export import Algo
from .model import CubeState
from .constant import C


class Al(Algo):
    def search_main(self, s: CubeState):
        states = s.bfs()
        return states[C.init_mask][0]
