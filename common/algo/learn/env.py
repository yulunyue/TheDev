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

    def do(self,action):
        raise Exception(f"{self.__class__}.do not impl")

class Algo:
    def __init__(self):
        pass
    
    def set_env(self,env):
        self.env:Env=env
        return self
    
    def load(self,num_episodes=1000,epsilon=0.1):
        self.num_episodes=num_episodes
        self.epsilon=epsilon

    def run_step(self,num):
        pass

    def run(self):
        rewards_record=[]
        for episode in range(self.num_episodes):
            self.env.reset()
            rewards_record.append(self.run_step(episode))
        return rewards_record