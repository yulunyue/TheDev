class Env:
    def __init__(self):
        self.actions=[]
        self.size=0
        self.init_state=0
        self.reset()
    def reset(self):
        return self

    def get_actions(self):
        return self.actions
    
    def get_regret(self,action):
        raise Exception("todo")
    
    def do(self,action):
        raise Exception(f"{self.__class__}.do not impl")

class Algo:
    def __init__(self):
        pass
    
    def set_env(self,env):
        self.env:Env=env
        return self
    
    def load(self,num_episodes=1000):
        self.num_episodes=num_episodes
    
    def get_action(self,*args):
        raise Exception("todo")

    def run_one_step(self,episode,action,reward)->int:
        raise Exception("todo")

    def run(self,with_draw=True):
        regrets_record=[]
        rewards_record=[]
        regret=0
        reword=0
        for episode in range(self.num_episodes):
            self.env.reset()
            action = self.get_action(episode)
            r=self.env.do(action)
            reword+=r
            regret+=self.run_one_step(episode,action,r)
            rewards_record.append(reword)
            regrets_record.append(regret)
        if with_draw:
            self.draw(dict(rewards=rewards_record,regrets=regrets_record))
    
    
    def draw(self,data):
        from common.third_util.draw import Draw
        Draw().draw_line([[
            v,None,k
        ] for k,v in data.items()]).save(f"data/log/{self.__class__.__name__}.jpg")