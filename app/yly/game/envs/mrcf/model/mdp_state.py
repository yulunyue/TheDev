from common.algo.search.state import np
from common.util.export import List, Dict
from .constant import C


class Action:
    def __init__(self, dst, p):
        self.dst: "MdpState" = dst
        self.p = p


class Policy:
    def __init__(self, key, reward):
        self.key = key
        self.reward = reward
        self.actions: List[Action] = []

    def add_action(self, dst, p):
        self.actions.append(Action(dst, p))


class MdpState:
    def __init__(self, k):
        self.k = k
        self.policys: List[Policy] = []


class MarkovDecisionProcess:
    def __init__(self):
        self.n = 5
        self.states = [MdpState(i) for i in range(self.n)]

        for k, v in C.P.items():
            a, b, c = k.split("-")
            key = f"{a}-{b}"
            p = Policy(key, C.R[key])
            p.add_action(self.states[int(c[1]) - 1], v)
            self.states[int(a[1]) - 1].policys.append(p)

    def get_mrp_form_mdp(self, pi: Dict[str, int]):
        ans = [[0] * self.n for _ in range(self.n)]
        for k, v in pi.items():
            a, b = k.split("-")
            s = self.states[int(a[1]) - 1]
            for p in s.policys:
                for a in p.actions:
                    ans[s.k][a.dst.k] += a.p * v
        return ans

    def get_reawrd(self, pi):
        ret = []
        for s in self.states:
            ret.append(0)
            for p in s.policys:
                ret[-1] += p.reward * pi[p.key]
        return ret

    def use_policy(self, po):
        p = [[0 for j in range(self.K)] for i in range(self.K)]
        self.reward = [0] * self.K
        for i in range(self.K):
            for a in self.actions:
                policy = self.S[i] + "-" + a
                if policy not in po:
                    continue
                self.reward[i] += po[policy] * self.R.get(policy, 0)
                for j in range(self.K):
                    s = policy + "-" + self.S[j]
                    if s in self.P_STATE:
                        p[i][j] = self.P_STATE[s] * po[policy]
        self.P = np.array(p)
        return self.computer()

    def calc_value(self, state, action_id, *args):
        s = self.S[state] + "-" + self.actions[action_id]
        ans = self.R[s]
        c2 = []
        for i in range(self.K):
            s1 = s + "-" + self.S[i]
            c2.append(self.P_STATE.get(s1, 0))
        c = np.dot(np.array(c2).reshape(1, self.K), self.V)
        return f"{s}:{ans+self.gamma*c[0][0]}"

    def use_p1(self):
        self.V = self.use_policy(self.get_policy1())
        return self.calc_value(3, 6)

    def sample(self, timestep_max=20, number=200):
        S, A, P, R, gamma = self.mdp
        episodes = []
        Pi = self.get_policy1()
        for _ in range(number):
            episode = []
            timestep = 0
            s = S[np.random.randint(self.K - 1)]
            while s != "s5" and timestep <= timestep_max:
                timestep += 1
                s_a = [f"{s}-{a}" for a in A]
                a = random_select(s_a, lambda v: Pi.get(v, 0))
                r = R.get(a, 0)
                s_next = random_select(S, lambda v: P.get(a + "-" + v, 0))
                episode.append((s, a, r, s_next))
                s = s_next
            episodes.append(episode)
        return episodes

    def mc(self, gamma=0.5):
        episodes = self.sample()
        ct = defaultdict(int)
        vt = defaultdict(int)
        for episode in episodes:
            g = 0
            for i in range(len(episode) - 1, -1, -1):
                s, a, r, s_next = episode[i]
                g = r + g * gamma
                ct[s] += 1
                vt[s] = vt[s] + (g - vt[s]) / ct[s]
        return dict(vt)

    def occu(self, s="s4", a="s4-概率前往", gamma=0.5, timestep_max=40):
        total_time = np.zeros(timestep_max)
        occur_time = np.zeros(timestep_max)
        for episode in self.sample():
            for i in range(len(episode)):
                s_opt, a_opt, r, s_next = episode[i]
                total_time[i] += 1
                if s == s_opt and a == a_opt:
                    occur_time[i] += 1
        rbo = 0
        for i in range(timestep_max - 1, -1, -1):
            if total_time[i]:
                rbo += gamma**i * occur_time[i] / total_time[i]
        return (1 - gamma) * rbo
