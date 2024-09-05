import bdb


def test_fun(n):
    ret = 0
    for i in range(n):
        ret += i
    return ret


class PdbUtil:
    def __init__(self) -> None:
        self.bdb = bdb.Bdb()

    def test(self):
        ret = self.bdb.runcall(test_fun, 8)
        print(self.bdb, ret, self.bdb.format_stack_entry())


if __name__ == "__main__":
    PdbUtil().test()
