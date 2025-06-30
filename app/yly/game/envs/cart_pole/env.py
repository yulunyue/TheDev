from common.algo.export import Action, State


class CartPoleEnv:
    env = None

    def load(self):
        if self.env is None:
            import gymnasium as gym

            self.env = gym.make("CartPole-v1")
        return self.env.reset()[0]

    def step(self, a):
        return self.env.step(a)

    def __str__(self):
        return f"state_dim:{self.env.observation_space.shape[0]},action_dim:{self.env.action_space.n}"


CP_ENV = CartPoleEnv()


class CartAction(Action):
    def do(self, **kw):
        self.dst.state, reward, done, *args = CP_ENV.step(self.action)
        self.dst.set_done(done)
        self.set_reward(reward)
        return self


class CartPoleState(State):
    @classmethod
    def get_init_state(cls):
        return CartPoleState(CP_ENV.load())

    def gen_action(self, a):
        return CartAction(self, a, CartPoleState(None)).set_value(0)

    def get_actions_all(self):
        return list(range(CP_ENV.env.action_space.n))

    def reset(self):
        self.state = CP_ENV.load()
        return self
