from ..constant import C
from common.util.export import List, Dict
from app.yly.game.envs.tic_toc.shape.line import Line, LINES


class Cell:
    def __init__(self):
        self.value = 0
        self.p_lines: List[Line] = []

    def set_key(self, key):
        self.key = key
        return self
