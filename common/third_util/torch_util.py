import torch
import torch.nn.functional as TorchF
from torch.nn import Linear, Module
from common.util.export import File
from torch import Tensor
import json


class TorchNet:
    SAVE_DIR = "data/model"
    model_cls = Module

    def __init__(self, name):
        self.name = name or self.__class__.__name__
        self.save_path = File(f"{self.SAVE_DIR}/{name}.pt")
        self.init_net()

    def init_net(self):
        if self.save_path.exists():
            # example_input = torch.rand(1, 3, 224, 224)
            self.model: Module = torch.jit.load(self.save_path.path)
            print(torch.jit.script(self.model))
        else:
            self.model: Module = self.model_cls()

    def print_model_details(self):
        msgs = []
        total_params = 0
        for name, module in self.model.named_modules():
            num_params = sum(p.numel() for p in module.parameters())
            total_params += num_params

            msgs.append(f"层: {name}")
            msgs.append(f"  类型: {type(module).__name__}")

            # 输入相关属性
            if hasattr(module, "in_channels"):
                msgs.append(f"  输入通道: {module.in_channels}")
            if hasattr(module, "in_features"):
                msgs.append(f"  输入特征: {module.in_features}")

            # 输出相关属性
            if hasattr(module, "out_channels"):
                msgs.append(f"  输出通道: {module.out_channels}")
            if hasattr(module, "out_features"):
                msgs.append(f"  输出特征: {module.out_features}")

            msgs.append(f"  参数数量: {num_params}")
            msgs.append("-" * 30)
        for i, (name, layer) in enumerate(self.model.named_children()):
            msgs.append(f"第{i}层: {name}, 类型: {type(layer)}")
            if hasattr(layer, "in_channels"):
                msgs.append(f"输入通道数: {layer.in_channels}")
            if hasattr(layer, "in_features"):
                msgs.append(f"输入特征数: {layer.in_features}")
        msgs.append(f"总参数数量: {total_params}")
        return "\n".join(msgs)

    def view(self):
        return f"states:{self.model.state_dict()}"


class TorchDoubleNet:
    model_cls = TorchNet

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
