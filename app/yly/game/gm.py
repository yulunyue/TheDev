from typing import Dict
from common.service.http import Node
from app.yly.game.game_base import GameBase
from app.yly.game.gus_num.main import GusNum
from app.yly.game.table.main import TbGame
from app.yly.game.ab.main import AbGame
from app.yly.game.connect_four.main import CfGame
GAME:Dict[str,GameBase]=dict()
for cls in GameBase.__subclasses__():
    GAME[cls.__name__]=cls
    
def get_game(game_id,room_id):
    key = (game_id,room_id)
    if key not in Route.rooms:
        Route.rooms[key]=GAME[game_id](room_id)
    return Route.rooms[key]

class Route:
    rooms:Dict[str,GameBase] = dict()
    def do(self, room_id, game_id,user_id,tp,data):
        get_game(game_id,room_id).do_action(game_id,user_id,tp,data)
        return Node().to_json()