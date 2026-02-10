from common.util.export import (
    Module,
    get_log,
    THE_DEV_CONSTANT,
    File,
    List,
    Dict,
    ThreadManage,
    Thread,
    time,
)
from ..base_class.table_base import (
    TableBase,
)
from .task_config import TaskConfig


class Task:
    def __init__(self, name):
        self.source = TableBase[TaskConfig]().set_resource(name)
        self.main_thread = Thread(target=self.run)

    def loop(self):
        for t in self.source.filter():
            t.exec()
        self.source.save()
        return self

    def run(self):
        while True:
            self.loop()
            time.sleep(1)

    def start(self):
        self.main_thread.start()
        return self


TASK_MANAGER: Dict[str, Task] = dict()


def get_task(name="taskconfig") -> Task:
    if name not in TASK_MANAGER:
        TASK_MANAGER[name] = Task(name)
    return TASK_MANAGER[name]
