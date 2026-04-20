from common.tool.export import TASK_MANAGE
from common.util.export import time, logger


def fun_add(*args):
    time.sleep(1)
    return 2


class TestManage:
    def test_add_task(self):
        t = TASK_MANAGE.add_task(
            "test", fun_path="common.tool.task.manage_test::fun_add"
        )
        assert t.exec() == dict(value=2)
        t.save()
