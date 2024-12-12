
from typing import List,Dict
from common.service.http import Node,send_clients_mag,WEB_SOCKET_CLIENTS
AI_KEY='AI_KEY'
class GameBase:
    def __init__(self,room_id) -> None:
        self.state:Node = self.get_data()
        self.user:Dict[str,Node] =dict()
        self.reset()
    
    def login(self,user_id):
        if user_id in self.user:
            return
        self.user[user_id] = self.get_data()
        self.state.childs.append(self.user[user_id])
    
    def get_data(self):
        return Node()

    def reset(self):
        pass
    
    def start(self, **kwagrs):
        pass

    def notify_state(self):
        state = self.state.to_json()
        for key in list(self.user.keys()):
            if key == AI_KEY:
                continue
            elif key in WEB_SOCKET_CLIENTS:
                send_clients_mag(key,state)
            elif key in self.user:
                self.user.pop(key)



    