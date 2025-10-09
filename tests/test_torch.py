from common.third_util.torch_util import torch, TorchNet
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
        self.expect_ndarray(c, TEST_DATA3)
        self.expect(a.max(), 6)

    def test_auto(self):
        a = torch.tensor([1.0], requires_grad=True)
        b = a * 2
        self.expect_ndarray(a, [1.0])
        self.expect_ndarray(b, [2.0])
        self.expect(a.grad, None)
        self.expect(a.requires_grad, True)
        b.backward()
        self.expect_ndarray(a.grad, [2.0])
        self.expect_ndarray(a, [1.0])

        c = a + 1
        c.backward()
        self.expect_ndarray(a.grad, [3.0])
        self.expect_ndarray(c, [2.0])
        with torch.no_grad():
            d = a + 2
        e = a * 3
        e.backward()
        self.expect_ndarray(e, [3.0])
        self.expect_ndarray(a.grad, [6.0])

    def run_nn(self):
        class TestNN(torch.nn.Module):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fc1 = torch.nn.Linear(2, 2)
                self.fc2 = torch.nn.Linear(2, 1)

            def forward(self, x):
                x = torch.relu(self.fc1(x))
                x = self.fc2(x)
                return x

        model = TestNN()
        x = torch.randn(5, 2)
        y = torch.randn(5, 1)
        optim = torch.optim.Adam(model.parameters(), lr=0.001)
        loss_fn = torch.nn.MSELoss()
        for i in range(10000):
            optim.zero_grad()
            output = model(x)
            loss: torch.Tensor = loss_fn(output, y)
            loss.backward()
            optim.step()
            if i % 1000 == 999:
                logger.info(loss)

        self.expect_ndarray(model(x), y)

    def run_model(self):
        a = TorchNet("c4/model_fish")
        logger.debug(a.view())


if __name__ == "__main__":
    TestTorch().run()
