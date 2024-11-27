from typing import Dict
from common.service.http import Node
from common.service.user import User
from .gus_num.main import GusNum
from .game_base import GameBase

GAME:Dict[str,GameBase]=dict()
for cls in GameBase.__subclasses__():
    GAME[cls.name]=cls()

class Room:
    def __init__(self) -> None:
        self.users:Dict[str,User]=dict()
    
    def add_user(self,user_name):
        if user_name in self.users:
            return
        self.users[user_name]=User(user_name)
    
    def do_action(self,game_id,tp,data):
        GAME[game_id].do_action(self.users,tp,data)

def get_room(room_id):
    if room_id not in Route.rooms:
        Route.rooms[room_id]=Room()
    return Route.rooms[room_id]

class Route:
    rooms:Dict[str,Room] = dict()
    def join_room(self,room_id,user_name):
        get_room(room_id).add_user(user_name)
        return Node().to_json()
    
    def do_room_action(self, room_id, game_id, action):
        get_room(room_id).do_action(game_id,action)
        return Node().to_json()