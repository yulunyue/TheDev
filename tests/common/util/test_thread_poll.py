from common.util.export import ThreadManage, TestBase, time


def thread_func_test(m):
    time.sleep(m)
    return m


class TestThreadPoll(TestBase):
    def test_base(self):
        manage = ThreadManage()
        result = manage.run(thread_func_test, [0.4, 0.3, 0.1])
        self.expect(result, [0.1, 0.3, 0.4])
