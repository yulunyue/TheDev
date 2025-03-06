from common.algo.learn.env import Env,Algo
import numpy as np

class EpsilonGreedy(Algo):
    regret=0
    def load(self, num_episodes=5000, epsilon=0.01,init_prob=1.0):
        self.estimates = np.array([init_prob]*len(self.env.actions))
        self.counts=np.zeros(len(self.env.actions))
        self.epsilon=epsilon
        return super().load(num_episodes)
    def get_action(self, *args):
        if np.random.random()<self.epsilon:
            k=np.random.randint(0,len(self.env.actions))
        else:
            k=np.argmax(self.estimates)
        return k
    
    def run_one_step(self, episode, k, reward):
        self.estimates[k] += 1.0/(self.counts[k]+1)*(reward-self.estimates[k])
        self.counts[k]+=1
        return self.env.get_regret(k)
    
    def __str__(self):
        return ",".join(["%.2f"%float(v) for v in self.estimates])
