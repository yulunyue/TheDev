from common.algo.learn.env import Env
import numpy as np
class Bandit(Env):
    k=10
    def reset(self):
        self.probs=np.random.uniform(self.k)
        