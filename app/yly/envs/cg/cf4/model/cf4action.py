from common.algo.export import Action

from .constant import C
from typing import List, Dict


class F4Action(Action):
    def __init__(self, src, action, done):
        super().__init__(src, action)
