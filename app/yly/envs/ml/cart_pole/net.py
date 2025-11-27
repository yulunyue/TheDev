from common.third_util.torch_util import torch, TorchDoubleNet
from .constant import C


class NetBase(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(C.STATE_DIM, C.NET_BASE_HIDDEN_DIM)
        self.fc2 = torch.nn.Linear(C.NET_BASE_HIDDEN_DIM, C.ACTION_DIM)

    def forward(self, x):
        x = torch.functional.F.relu(self.fc1(x))
        return self.fc2(x)
