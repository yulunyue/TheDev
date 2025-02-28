from common.algo.learn.env import Env,Algo
import numpy as np
class Bernoulli(Algo):
    regret=0
    def load(self, num_episodes=1000, epsilon=0.1):
        self.estimates = [0]*len(self.env.actions)
        return super().load(num_episodes, epsilon)
    
    def run_step(self, episode):
        a=self.get_action()
        reword=self.env.do(a)
        self.estimates[a]+=reword
        return reword
    
    def get_action(self):
        if np.random.random()<self.epsilon:
            return np.random.randint(0,len(self.env.actions))
        return np.argmax(self.estimates)