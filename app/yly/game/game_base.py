
from typing import List,Dict
from common.service.http import Node,send_clients_mag,WEB_SOCKET_CLIENTS
class User:
    def __init__(self,user_id) -> None:
        self.user_id = user_id
        self.room_id=""
        self.game:GameBase = None

    def set_room_id(self,room_id):
        self.room_id = room_id
        return self
    
    def set_game(self,game):
        self.game = game
        return self

AI_KEY='AI_KEY'
class GameBase:
    users:Dict[str,User] = dict()
    def __init__(self,room_id) -> None:
        self.game_id=self.__class__.__name__
        self.room_id:str=room_id
        self.state:Node = self.get_state()
        self.room_user=set()
        self.reset()
    
    def login(self,user_id,**kw):
        if user_id not in self.users:
            self.users[user_id]=User(user_id)
        self.room_user.add(user_id)
            
    
    def get_state(self):
        return Node()

    def reset(self):
        pass
    
    def start(self, **kwagrs):
        pass

    def notify_state(self):
        state = self.state.to_json()
        for key in list(self.room_user):
            if key == AI_KEY:
                continue
            elif key in WEB_SOCKET_CLIENTS:
                send_clients_mag(key,dict(
                    type=f'{self.game_id}_{self.room_id}',
                    data=state
                ))
            else:
                self.room_user.remove(key)
                
    def do_action(self,game_id,user_id,tp,data):
        getattr(self,tp)(user_id=user_id,**data)
        self.notify_state()


    