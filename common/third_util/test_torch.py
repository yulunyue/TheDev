from common.third_util.ml.torch_util import torch, F
from common.util.export import TestBase, logger


class TestTorch(TestBase):
    def expect(self, a, expect_value=True, info="", stacklevel=2):
        if isinstance(a, torch.Tensor):
            a = torch.allclose(a, expect_value)
            expect_value = True
        return super().expect(a, expect_value, info, stacklevel)

    def test_base(self):
        TEST_DATA1 = [
            [1, 2, 3],
            [4, 2, 6],
        ]
        TEST_DATA2 = [
            [2, 3, 2],
            [1, 2, 1],
        ]
        TEST_DATA3 = [
            [2, 6, 6],
            [4, 4, 6],
        ]

        a = torch.tensor(TEST_DATA1)
        b = torch.tensor(TEST_DATA2)
        c = a * b
        self.expect(a.sum().item(), 18)
        self.expect(c.tolist(), TEST_DATA3)
        self.expect(a.max().item(), 6)

    def test_log_soft_max(self):
        logits = torch.tensor([[1.0, 2.0, 3.0], [1.0, 1.0, 1.0]])
        result = F.log_softmax(logits, dim=1)

    def test_dim(self):
        """
        dim（维度）指定了沿着哪个轴进行操作：
        dim=0：沿着行（垂直）方向操作
        dim=1：沿着列（水平）方向操作
        dim=2：沿着第三个维度操作（3D张量）
        """
        tensor_1d = torch.tensor([1, 2, 3, 4])
        self.expect(tensor_1d.dim(), 1)
        self.expect(tensor_1d.shape, torch.Size([4]))
        s1 = tensor_1d.sum(dim=0)
        self.expect(s1.shape, torch.Size([]))
        self.expect(s1.item(), 10)
        tensor_3d = torch.tensor(
            [
                [
                    [1, 2, 3, 4],
                    [3, 4, 3, 4],
                    [5, 6, 3, 4],
                ],
                [
                    [7, 8, 3, 4],
                    [9, 10, 3, 4],
                    [11, 12, 3, 4],
                ],
            ]
        )
        self.expect(tensor_3d.shape, torch.Size([2, 3, 4]))
        s1 = tensor_3d.sum(dim=0)
        self.expect(s1.shape, torch.Size([3, 4]))
        self.expect(
            s1,
            torch.Tensor(
                [
                    [8, 10, 6, 8],
                    [12, 14, 6, 8],
                    [16, 18, 6, 8],
                ],
            ).long(),
        )
        s2 = tensor_3d.sum(dim=1)
        self.expect(s2.shape, torch.Size([2, 4]))
        self.expect(
            s2,
            torch.Tensor(
                [
                    [9, 12, 9, 12],
                    [27, 30, 9, 12],
                ]
            ).long(),
        )

    def test_gather(self):
        """
        gather   函数是一个沿指定维度收集特定索引位置的值的操作。它的主要功能是根据索引张量从输入张量中提取对应位置的值。
        dim = 0 表示Y方向
        dim = 1 表示X方向
        """
        t = torch.tensor(
            [
                # 第一个样本
                [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
                # 第二个样本
                [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]],
            ]
        )
        index = torch.tensor(
            [
                [[0], [1], [0]],
                [[1], [0], [1]],
            ]
        )
        self.expect(
            t.gather(0, index).tolist(),
            [
                [[1], [17], [9]],  # [ t[0][0][0], t[1][1][0], t[0][2][0] ]
                [[13], [5], [21]],  # [ t[1][0][0], t[0][1][0], t[1][2][0] ]
            ],
        )
        self.expect(
            t.gather(1, index).tolist(),
            [
                [[1], [5], [1]],  # [ t[0][0][0], t[0][1][0], t[0][0][0] ]
                [[17], [13], [17]],  # [ t[1][1][0], t[1][0][0], t[1][1][0] ]
            ],
        )
        self.expect(
            t.gather(2, index).tolist(),
            [
                [[1], [6], [9]],  # [ t[0][0][0], t[0][1][1], t[0][2][0] ]
                [[14], [17], [22]],  # [ t[1][0][1], t[1][1][0], t[1][2][1] ]
            ],
        )
