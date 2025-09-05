from common.third_util.export import TorchNet, TorchF, Linear, TorchDoubleNet, torch
from .constant import C


class NetBase(TorchNet):
    def init_net(self):
        self.fc1 = Linear(C.STATE_DIM, C.NET_BASE_HIDDEN_DIM)
        self.fc2 = Linear(C.NET_BASE_HIDDEN_DIM, C.ACTION_DIM)

    def forward(self, x):
        x = TorchF.relu(self.fc1(x))
        return self.fc2(x)


class Net2(TorchDoubleNet):
    model_cls = NetBase
