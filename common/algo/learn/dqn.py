from common.algo.learn.sarse.qlearning import Qlearning, Action, State, np
from common.third_util.torch_util import TorchDoubleNet
from .util.replay_buff import ReplayBuffer
from common.util.fp import File


class Dqn(Qlearning):
    """
    https://hrl.boyuai.com/
    """

    def set_model(self, model, **kw) -> "Dqn":
        self.model: TorchDoubleNet = model
        # self.replay_buffer = ReplayBuffer(10000)
        return self

    # def update_action(self, a: Action):
    #     self.replay_buffer.add(a.src.state, a.action, a.reward, a.dst.state, a.dst.done)
    #     if self.replay_buffer.size() > 500:
    #         self.update_net(**self.replay_buffer.sample(64))

    def get_max_action(self, state: State):
        action = self.model.get_max_action(state.state)
        return state.get_action(action)

    def update_net(self, states, actions, next_states, rewards, dones):
        self.model.update_net(states, actions, next_states, rewards, dones)
        # states = torch.tensor(states, dtype=torch.float)
        # actions = torch.tensor(actions).view(-1, 1)
        # rewards = torch.tensor(rewards, dtype=torch.float).view(-1, 1)
        # next_states = torch.tensor(next_states, dtype=torch.float)
        # dones = torch.tensor(dones, dtype=torch.float).view(-1, 1)

    def train(self, state):
        self.records_rewward = []
        ret = super().train(state)
        from common.third_util.draw import Draw

        Draw().draw_line(self.records_rewward).save(
            self.get_tmp_file_path("result.svg")
        )
        return ret

    def train_one(self, i, state):
        ret = super().train_one(i, state)
        self.records_rewward.append(len(self.actions))
        return ret
