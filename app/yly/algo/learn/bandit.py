from common.algo.learn.env import Env
from common.algo.learn.bernoulli import EpsilonGreedy,Algo
from common.algo.manage import SolutionBase
import random
import numpy as np
class Bandit(Env):
    k=10
    def reset(self):
        self.probs=np.random.uniform(size=self.k)
        # self.probs=np.array([0.1]*self.k)
        self.max_idx=self.probs.argmax()
        self.actions=list(range(self.k))

    def do(self, action):
        return 1 if np.random.random()<=self.probs[action] else 0
    
    def get_regret(self,action):
        return self.probs[self.max_idx]-self.probs[action]
    def __str__(self):
        return ",".join(["%.2f"%float(v) for v in self.probs])
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(tp='ep',num_episodes=5000)
        ]
    
    def init(self,tp,**kwagrs):
        self.env=Bandit()
        self.actor:Algo=dict(ep=EpsilonGreedy)[tp]()
        self.actor.set_env(self.env).load(**kwagrs)
    
    def execute(self,**kw):
        self.log(self.env)
        self.actor.run()
        self.log(self.actor)

if __name__=="__main__":
    np.random.seed(7)
    Solution().run()
        