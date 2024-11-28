
from typing import List,Dict
from common.service.http import Node,send_clients_mag
class GameBase:
    def __init__(self,room_id) -> None:
        self.state = Node(type=room_id)
        self.user:Dict[str,Node] =dict()
        self.init()
    
    def login(self,user_id):
        if user_id in self.user:
            return
        self.user[user_id] = Node(key=user_id)
        self.state.childs.append(self.user[user_id])
        

    def init(self):
        pass
    
    def start(self, **kwagrs):
        pass

    def notify_state(self):
        state = self.state.to_json()
        send_clients_mag(self.user.keys(),state)
