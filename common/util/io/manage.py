from .base import Io
from typing import Dict
from ..node import Node


class Manage:
    def __init__(self):
        self.io_map: Dict[str, Io] = dict()

    def hander_msg(self, io, msg: Node):
        self.io_map[msg.key] = io
        return self


IO_MANAGE = Manage()
