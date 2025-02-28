from common.algo.learn.env import Env
from common.algo.learn.bernoulli import Bernoulli
from common.algo.manage import SolutionBase
import numpy as np
class Bandit(Env):
    k=10
    def reset(self):
        self.probs=np.random.uniform(self.k)
        

class Solution(SolutionBase):
    def get_cases(self):
        return dict(
            result=""
        )
    def execute(self):
        self.b=Bernoulli(Bandit())
        self.b.run()

if __name__=="__main__":
    SolutionBase().run()
        