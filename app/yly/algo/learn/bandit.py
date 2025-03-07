from common.algo.learn.env import Env
from common.algo.learn.bernoulli import EpsilonGreedy,Algo,DecayingEpsilonGreedy,Ucb,ThompsonSampling
from common.algo.manage import SolutionBase
from typing import List
import numpy as np
class Bandit(Env):
    K=10
    def __init__(self):
        self.probs=np.random.uniform(size=self.K)
        self.max_idx=self.probs.argmax()
        self.actions=list(range(self.K))
     
    
    def do(self, action):
        return 1 if np.random.rand()<self.probs[action] else 0
    
    def get_regret(self,action):
        return self.probs[self.max_idx]-self.probs[action]
    
    def __str__(self):
        return ",".join(["%.3f"%float(v) for v in self.probs])
    
class Solution(SolutionBase):
    def get_cases(self):
        return [
            dict(tp='ep',epsilon=0.01),
            dict(tp='de',epsilon=1),
            dict(tp='ucb'),
            dict(tp='ts')
        ]
    
    def load(self):
        self.env = Bandit()
        self.log(self.env)
    
    def execute(self,tp,**kw):
        actor:Algo=dict(
            ep=EpsilonGreedy,
            de=DecayingEpsilonGreedy,
            ucb=Ucb,
            ts=ThompsonSampling,
        )[tp]()
        actor.set_env(self.env).load(**kw)
        ret = actor.run()
        self.log(actor,actor.rewards_record[-1])
        return ret 
    
    def run_finish(self,results:List[EpsilonGreedy]):
        from common.third_util.draw import Draw
        Draw().draw_line([[
            r.regrets_record,None,f'{r.__class__.__name__}'
        ] for r in results]).save(f"data/log/{self.__class__.__name__}.jpg")


if __name__=="__main__":
    np.random.seed(3)
    Solution().run()
        