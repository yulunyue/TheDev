from typing import Dict
from common.service.http import Node
from common.service.user import User
from .gus_num.main import GusNum
from .game_base import GameBase

GAME:Dict[str,GameBase]=dict()
for cls in GameBase.__subclasses__():
    GAME[cls.__name__]=cls

class Room:
    def __init__(self,room_id) -> None:
        self.room_id = room_id
        self.games:Dict[str,GameBase]=dict()
    
    def get_game(self,game_id):
        if not game_id in self.games:
            self.games[game_id]=GAME[game_id](self.room_id)
        return self.games[game_id]
        
    def do_action(self,game_id,user_id,tp,data):
        game=self.get_game(game_id)
        getattr(game,tp)(user_id=user_id,**data)
        game.notify_state()
    
def get_room(room_id):
    if room_id not in Route.rooms:
        Route.rooms[room_id]=Room(room_id)
    return Route.rooms[room_id]

class Route:
    rooms:Dict[str,Room] = dict()
    def do(self, room_id, game_id,user_id,tp,data):
        get_room(room_id).do_action(game_id,user_id,tp,data)
        return Node().to_json()