from typing import Dict
from common.service.http import Node
from app.yly.game.game_base import GameBase
from common.util.fp import File
from common.util.module import Module
class TbGame(GameBase):
    def get_state(self):
        if self.room_id.endswith('.json'):
            return File(self.room_id).read_file()
        path,name=self.room_id.split('|')
        return Module().load_module(name,path)