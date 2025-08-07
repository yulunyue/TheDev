from common.util.export import (
    get_function_info,
    TestBase,
    ThreadManage,
    logger,
    re_search,
    Module,
    File,
    TypeVar,
    List,
    Generic,
)
import threading
import time

thread_local_val = threading.local()


class D:
    def get_value(self):
        pass


def cls_gen(info) -> TypeVar(D):
    class C(D):
        type_info = dict(type="select", info=info)

    return C


class TestCls:
    def test_fun(self, a: int, c: cls_gen("xx"), b=2):
        return a + b + c


T = TypeVar("T")


class Stack(Generic[T]):
    items: List[T]


class TestUtil(TestBase):
    def test_fun(self):
        c = TestCls()
        a = get_function_info(Stack[int])
        logger.info(a)
        info = get_function_info(c.test_fun)
        self.expect(info.data["kwargs"], dict(a=None, b=2))

    def test_debug(self):
        self.test_fun()

    def test_cls(self):
        self.expect(TestCls.__module__, "??")

    def test_thread(self):
        def fun1(v):
            time.sleep(v)
            return v

        t = [0.2, 0.1, 0.15]
        t1 = ThreadManage().run(fun1, t)
        self.expect(t1, sorted(t))

        def get_local(*args):
            logger.info([thread_local_val, hasattr(thread_local_val, "v")])
            return

        def set_local(v):
            thread_local_val.v = v
            logger.info([thread_local_val, hasattr(thread_local_val, "v")])
            return ThreadManage().run(get_local, t)

        ThreadManage().run(set_local, t)

    def test_re(self):
        self.expect(re_search(".*ab.*", "aabbcc") is not None)

    def test_file(self):
        path = "data/temp/zip_test"
        File(path).zip()
        File(path + ".zip").unzip()


if __name__ == "__main__":
    TestUtil().run()
