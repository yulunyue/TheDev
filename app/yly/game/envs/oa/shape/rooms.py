
class Rooms:
    ROOM_NUM=12
    def reset(self):
        self.roomall=[4]*self.ROOM_NUM
        self.actions=list(range(6))
        return self
    
    def set_rooms(self,rooms):
        for i,v in enumerate(rooms):
            self.roomall[i]=v
        return self
    
    def get_action(self):
        for a in self.actions:
            if self.roomall[a]:
                return a

    def do_action(self,action):
        for i in range(self.roomall[action]):
            self.roomall[(action+i+1)%self.ROOM_NUM]+=1
        self.roomall[action]=0
        return self
