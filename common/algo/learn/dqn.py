from common.algo.learn.env import Env
from common.algo.learn import np
class Dqn:
    def __init__(self,env:Env,num_episodes=500,gamma_discount=0.9,epsilon=0.1,alpha=0.5):
        self.env:Env=env
        self.num_episodes=num_episodes
        self.gamma_discount=gamma_discount
        self.epsilon = epsilon
        self.alpha=alpha
    def run(self):
        self.q_table=np.zeros((len(self.env.actions),self.env.size))
        rewards_record=[]
        for episode in range(self.num_episodes):
            self.env.reset()
            last_reward=self.env.reward
            last_state=self.env.state
            rewards_sum=0
            game_over=False
            while not game_over:
                actions=self.env.get_actions()
                action=self.epsilon_greedy_policy(actions)
                game_over,reward=self.env.do(action)
                rewards_sum+=reward
                self.update_qtable(last_state,action,last_reward,reward)
                last_reward,last_state=reward,self.env.state
            rewards_record.append(reward)
        return self.q_table,rewards_record
                

    def epsilon_greedy_policy(self, actions):
        decide_explore_exploit=np.random.random()
        if decide_explore_exploit<self.epsilon:
            action=np.random.choice(len(actions))
        else:
            action=np.argmax(self.q_table[:,self.env.state])
        return action
    
    def update_qtable(self,state,action,reward,next_reward):
        alpha_value = reward + (self.gamma_discount * next_reward) - self.q_table[action, state]
        self.q_table[action,state]+=self.alpha*alpha_value

