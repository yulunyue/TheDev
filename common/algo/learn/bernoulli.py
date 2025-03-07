from common.algo.learn.env import Env,Algo
import numpy as np

class EpsilonGreedy(Algo):
    def load(self, num_episodes=5000, epsilon=0.01,init_prob=1.0):
        self.estimates = np.array([init_prob]*len(self.env.actions))
        self.counts = np.zeros(len(self.env.actions))
        self.epsilon=epsilon
        return super().load(num_episodes)
    
    def get_action(self, *args):
        if np.random.rand()<self.epsilon:
            k=np.random.randint(0,len(self.env.actions))
        else:
            k=np.argmax(self.estimates)
        return k
    
    def run_one_step(self, episode, k, reward):
        self.counts[k] += 1
        self.estimates[k] += 1. / self.counts[k]*(reward-self.estimates[k])
        return self.env.get_regret(k)
    
    def __str__(self):
        return ",".join(["%.3f"%v for v in self.estimates])

class DecayingEpsilonGreedy(EpsilonGreedy):
    total_count=0
    def get_action(self, *args):
        self.total_count+=1
        if np.random.rand()<self.epsilon/self.total_count:
            k=np.random.randint(0,len(self.env.actions))
        else:
            k=np.argmax(self.estimates)
        return k
    
class Ucb(DecayingEpsilonGreedy):
    def load(self, num_episodes=5000, coef=1):
        self.coef=coef
        return super().load(num_episodes)
    def get_action(self, *args):
        self.total_count+=1
        ucb=self.estimates + self.coef *np.sqrt(
            np.log(self.total_count)/(2*(self.counts+1))
        )
        return np.argmax(ucb)

class ThompsonSampling(Algo):
    def load(self, num_episodes=5000):
        self.a=np.ones(self.env.K)
        self.b=np.ones(self.env.K)
        return super().load(num_episodes)
    
    def get_action(self, *args):
        samples=np.random.beta(self.a,self.b)
        return np.argmax(samples)
    
    def run_one_step(self, episode, action, reward):
        self.a[action]+=reward
        self.b[action]+=(1-reward)
        return self.env.get_regret(action)
        
