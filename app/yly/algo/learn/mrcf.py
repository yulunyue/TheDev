from common.algo.search.algo import Env,np,random_select
from common.algo.manage import SolutionBase,View,bisect,defaultdict,Dict,List,MOD,inf,heapq,functools,null,false,true

class Mrp(Env):
    def __init__(self):
        self.P=np.array([
            [0.9, 0.1, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.0, 0.5, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.6, 0.0, 0.4],
            [0.0, 0.0, 0.0, 0.0, 0.3, 0.7],
            [0.0, 0.2, 0.3, 0.5, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        ])
        self.reward=[-1, -2, -2, 10, 1, 0]
        self.actions=list(range(len(self.reward)))
        self.K=len(self.reward)

    def computer_return(self,chains,start=0,gamma=0.5):
        ret=0
        for i in range(len(chains)-1,start-1,-1):
            ret=gamma*ret+self.reward[chains[i]-1]
        return ret
    
    def computer(self,gamma=0.5,**kw):
        reward=np.array(self.reward).reshape((-1,1))
        eye=np.eye(self.K,self.K)-gamma*self.P
        return np.dot(np.linalg.inv(eye),reward)


    
class Mdp(Mrp):
    def __init__(self,gamma=0.5):
        self.S = ["s1", "s2", "s3", "s4", "s5"]  # 状态集合
        self.K = len(self.S)
        self.actions = ["保持s1", "前往s1", "前往s2", "前往s3", "前往s4", "前往s5", "概率前往"]  # 动作集合
        # 状态转移函数
        self.P_STATE = {
            "s1-保持s1-s1": 1.0,
            "s1-前往s2-s2": 1.0,
            "s2-前往s1-s1": 1.0,
            "s2-前往s3-s3": 1.0,
            "s3-前往s4-s4": 1.0,
            "s3-前往s5-s5": 1.0,
            "s4-前往s5-s5": 1.0,
            "s4-概率前往-s2": 0.2,
            "s4-概率前往-s3": 0.4,
            "s4-概率前往-s4": 0.4,
            "s5-前往s5-s5":1.0
        }
        # 奖励函数
        self.R = {
            "s1-保持s1": -1,
            "s1-前往s2": 0,
            "s2-前往s1": -1,
            "s2-前往s3": -2,
            "s3-前往s4": -2,
            "s3-前往s5": 0,
            "s4-前往s5": 10,
            "s4-概率前往": 1
        }
        self.gamma=gamma
        self.mdp=(self.S,self.actions,self.P_STATE,self.R,gamma)
    
    def get_policy1(self):
        return {
            "s1-保持s1": 0.5,
            "s1-前往s2": 0.5,
            "s2-前往s1": 0.5,
            "s2-前往s3": 0.5,
            "s3-前往s4": 0.5,
            "s3-前往s5": 0.5,
            "s4-前往s5": 0.5,
            "s4-概率前往": 0.5,
            "s5-前往s5": 1,
        }
    
    def get_policy2(self):
        return {
            "s1-保持s1": 0.6,
            "s1-前往s2": 0.4,
            "s2-前往s1": 0.3,
            "s2-前往s3": 0.7,
            "s3-前往s4": 0.5,
            "s3-前往s5": 0.5,
            "s4-前往s5": 0.1,
            "s4-概率前往": 0.9,
            "s5-前往s5": 1,
        }
    
    def use_policy(self,po):
        p=[[0 for j in range(self.K)] for i in range(self.K)]
        self.reward=[0]*self.K
        for i in range(self.K):
            for a in self.actions:
                policy=self.S[i]+"-"+a
                if policy not in po:
                    continue 
                self.reward[i]+=po[policy]*self.R.get(policy,0)
                for j in range(self.K):
                    s=policy+'-'+self.S[j]
                    if s in self.P_STATE:
                        p[i][j]=self.P_STATE[s]*po[policy]
        self.P=np.array(p)
        return self.computer()

    def calc_value(self, state, action_id, *args):
        s=self.S[state]+"-"+self.actions[action_id]
        ans=self.R[s]
        c2=[]
        for i in range(self.K):
            s1=s+"-"+self.S[i]
            c2.append(self.P_STATE.get(s1,0))
        c=np.dot(np.array(c2).reshape(1,self.K),self.V)
        return f'{s}:{ans+self.gamma*c[0][0]}'

    def use_p1(self):
        self.V=self.use_policy(self.get_policy1())
        return self.calc_value(3,6)    
    
    def sample(self,timestep_max=20, number=200):
        S,A,P,R,gamma=self.mdp
        episodes=[]
        Pi=self.get_policy1()
        for _ in range(number):
            episode=[]
            timestep=0
            s=S[np.random.randint(self.K-1)]
            while s!='s5' and timestep<=timestep_max:
                timestep+=1
                s_a=[f'{s}-{a}' for a in A]
                a=random_select(s_a,lambda v:Pi.get(v,0))
                r=R.get(a,0)
                s_next=random_select(S,lambda v:P.get(a+"-"+v,0))
                episode.append((s,a,r,s_next))
                s=s_next
            episodes.append(episode)
        return episodes
    
    def mc(self,gamma=0.5):
        episodes=self.sample()
        ct=defaultdict(int)
        vt=defaultdict(int)
        for episode in episodes:
            g=0
            for i in range(len(episode)-1,-1,-1):
                s,a,r,s_next=episode[i]
                g=r+g*gamma
                ct[s]+=1
                vt[s]=vt[s]+(g-vt[s])/ct[s]
        return dict(vt)
    
    def occu(self,s='s4',a='s4-概率前往',gamma=0.5,timestep_max=40):
        total_time=np.zeros(timestep_max)
        occur_time=np.zeros(timestep_max)
        for episode in self.sample():
            for i in range(len(episode)):
                s_opt,a_opt,r,s_next=episode[i]
                total_time[i]+=1
                if s==s_opt and a==a_opt:
                    occur_time[i]+=1
        rbo=0
        for i in range(timestep_max-1,-1,-1):
            if total_time[i]:
                rbo+=gamma**i * occur_time[i]/total_time[i]
        return (1-gamma)*rbo





class Solution(SolutionBase):
    def get_cases(self):
        return [
            # dict(tp="mrp",method="computer_return", chains=[1,2,3,6],result=-2.5),
            # dict(tp="mrp",method="computer",result=-2.5)
            dict(tp="mdp",method="occu",result='?')
        ]   

    def init(self, tp,*args, **kwargs):
        self.ins=dict(
            mrp=Mrp,
            mdp=Mdp
        )[tp]()

    def execute(self,method,result="",tp="",**kw):
        return getattr(self.ins,method)(**kw)


    


if __name__=='__main__':
    np.random.seed(0)
    Solution().run()