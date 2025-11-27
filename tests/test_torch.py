from common.third_util.torch_util import torch
from common.util.export import TestBase, logger


class TestTorch(TestBase):
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
        self.expect(a.sum(), 18)
        self.expect(c, TEST_DATA3)
        self.expect(a.max(), 6)

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
            t.gather(0, index),
            [
                [[1], [17], [9]],  # [ t[0][0][0], t[1][1][0], t[0][2][0] ]
                [[13], [5], [21]],  # [ t[1][0][0], t[0][1][0], t[1][2][0] ]
            ],
        )
        self.expect(
            t.gather(1, index),
            [
                [[1], [5], [1]],  # [ t[0][0][0], t[0][1][0], t[0][0][0] ]
                [[17], [13], [17]],  # [ t[1][1][0], t[1][0][0], t[1][1][0] ]
            ],
        )
        self.expect(
            t.gather(2, index),
            [
                [[1], [6], [9]],  # [ t[0][0][0], t[0][1][1], t[0][2][0] ]
                [[14], [17], [22]],  # [ t[1][0][1], t[1][1][0], t[1][2][1] ]
            ],
        )

    def test_auto(self):
        a = torch.tensor([1.0], requires_grad=True)
        b = a * 2
        self.expect(a, [1.0])
        self.expect(b, [2.0])
        self.expect(a.grad, None)
        self.expect(a.requires_grad, True)
        b.backward()
        self.expect(a.grad, [2.0])
        self.expect(a, [1.0])
        self.expect(a.requires_grad, True)
        c = a + 1
        self.expect(a.requires_grad, True)
        c.backward()
        self.expect(a.grad, [3.0])
        self.expect(c, [2.0])
        with torch.no_grad():
            d = a + 2
        e = a * 3
        e.backward()
        self.expect(e, [3.0])
        self.expect(a.grad, [6.0])


if __name__ == "__main__":
    TestTorch().run()
