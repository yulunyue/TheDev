from common.util.export import TestBase, logger
from common.tool.export import BP, BpNode


def mul(a: int, b: int):
    return a * b


def add(a: int, b: int):
    return a + b


def sub(a: int, b: int):
    return a - b


class TestBp(TestBase):
    def test_demo(self):
        BP.register_func(mul=mul, add=add, sub=sub)
        n = BP.load_from_file("data/bp/demo.txt")
        self.expect(n.get_value(), 40)

    def debug(self):
        return self.test_demo()


if __name__ == "__main__":
    TestBp().run()
