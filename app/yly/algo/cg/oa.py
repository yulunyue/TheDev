from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true


class Env:
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

class Solution(SolutionBase):
    uri='https://www.codingame.com/ide/puzzle/oware-abapa'
    def get_cases(self):
        return [

        ]
    
    def init(self):
        self.env=Env().reset()
   
    def execute(self):
        action=self.env.get_action()
        self.env.do_action(action)
        return action


    def exec(self):
        self.init()
        while True:
            self.env.set_rooms(self.il())
            self.output(self.execute())



if __name__=='__main__':
    Solution().run()