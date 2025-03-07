from typing import List
from .state import State,inf
class Algo:
    state_count=0
    
    def set_env(self,env:State):
        self.env=env
        return self
    
    def load(self,num_episodes=5000):
        self.num_episodes=num_episodes
        
    def search_dp(self,state:State,depth=0):
        mvs:List[State]=state.get_nexts(depth)
        self.state_count+=1
        if not mvs:
            return state.calc_value(depth)
        state.value = -inf
        for action,next_state in mvs:
            value=-self.search_dp(next_state,depth-1)
            if value>state.value:
                state.value=value
                state.best_action=action
        return state.value
    
    def search(self,state,depth):
        self.state_count=0
        return self.search_dp(state,depth)
    
    def self_play(self,state:State):
        while not state.is_game_over():
            pass
    
    def run(self):
        self.regrets_record=[]
        self.rewards_record=[]
        regret=0
        reword=0
        self.env.reset()
        for episode in range(self.num_episodes):
            action = self.get_action(episode)
            r=self.env.do(action)
            reword+=r
            regret+=self.run_one_step(episode,action,r)
            self.rewards_record.append(reword)
            self.regrets_record.append(regret)
        return self