import torch
from common.util.export import File
import json

SAVE_DIR = "data/model"


def view(self):
    ans = []
    for k, s in self.model.state_dict().items():
        v: torch.Tensor = s
        ans.append(f"key:{k} shape:{v.shape} type:{v.dtype}")
    return "\n".join(ans)


class TorchDoubleNet:
    model_cls = torch.nn.Module

    def __init__(self):
        self.q_net = self.__class__.model_cls()
        self.target_q_net = self.__class__.model_cls()

    def load(
        self,
        learning_rate=0.002,
        gamma=0.9,
        update_target_freq=10,
        model_path="",
    ):
        self.gamma = gamma
        self.state_count = 0
        self.update_target_freq = update_target_freq

        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=learning_rate)
        self.model_file = File(model_path)
        if model_path:
            self.model_file.make_dir_if_not_exist()
            if self.model_file.exists():
                self.q_net.load_state_dict(torch.load(model_path))
        return self

    def get_max_action(self, state):
        s = torch.tensor(state, dtype=torch.float)
        t: Tensor = self.q_net(s)
        return t.argmax().item()

    def update_net(self, states, actions, rewards, next_states, dones):
        q_values: Tensor = self.q_net(states)
        q_values = q_values.gather(1, actions)
        max_next_q_values: Tensor = self.target_q_net(next_states)
        max_next_q_values = max_next_q_values.max(1)[0].view(-1, 1)
        q_targets = rewards + self.gamma * max_next_q_values * (1 - dones)
        loss = torch.mean(TorchF.mse_loss(q_values, q_targets))  # 均方误差损失函数
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.state_count += 1
        if self.state_count % self.update_target_freq:
            self.target_q_net.load_state_dict(self.q_net.state_dict())

    def save(self):
        torch.save(self.q_net.state_dict(), self.model_file.path)


class TorchUtil:
    pass
