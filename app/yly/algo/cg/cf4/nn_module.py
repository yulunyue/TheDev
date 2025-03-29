from torch import nn


class ConnectFourNet(nn.Module):
    def __init__(self):
        super().__init__()
        # 特征提取层
        self.conv_block = nn.Sequential(
            nn.Conv2d(2, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
        )

        # 策略头（选择列的概率分布）
        self.policy_head = nn.Sequential(
            nn.Conv2d(128, 2, 1),
            nn.BatchNorm2d(2),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(2 * 6 * 7, 7),
            nn.Softmax(dim=-1),
        )

        # 价值头（局面评估）
        self.value_head = nn.Sequential(
            nn.Conv2d(128, 1, 1),
            nn.BatchNorm2d(1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(6 * 7, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Tanh(),
        )  # 输出范围[-1,1]

    def forward(self, x):
        x = self.conv_block(x)
        p = self.policy_head(x)
        v = self.value_head(x)
        return p, v
