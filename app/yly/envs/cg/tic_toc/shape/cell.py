from ..constant import C
from common.util.export import List, Dict
from app.yly.envs.cg.tic_toc.shape.line import Line, LINES


class Cell:
    def __init__(self,key):
        self.value = 0
        self.key = key
        self.p_lines: List[Line] = []

