from common.third_util.torch_util import torch
from common.util.export import TestBase, logger


TEST_DATA1 = [[1, 2, 3], [4, 2, 6]]
TEST_DATA2 = [[2, 3, 2], [1, 2, 1]]
TEST_DATA3 = [[2, 6, 6], [4, 4, 6]]


class TestTorch(TestBase):
    def test_base(self):
        a = torch.tensor(TEST_DATA1)
        b = torch.tensor(TEST_DATA2)
        c = a * b
        self.expect(a.sum(), 18)
        self.expect(c, TEST_DATA3)
        self.expect(a.max(), 6)

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
