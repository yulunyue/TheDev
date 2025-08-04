from common.util.export import Module, get_log
from common.tool.base_class.table_base import (
    TableBase,
    StrModel,
    NumberModel,
    ConfigBase,
    TableConfig,
)

logger = get_log("task")
import _thread
import time
from typing import Dict, List


class TaskConfig(TableConfig):

    def __init__(self):
        self.module_name = StrModel()
        self.fun_name = StrModel()
        self.root_path = StrModel()
        self.args = StrModel()
        self.wait_time = NumberModel()
        super().__init__()

    def load(self, **kw):
        super().load(**kw)
        self.fun = Module().load_module(self.module_name, self.root_path, self.fun_name)
        self.last_begin_t = 0
        self.last_finish_t = 0
        self.result = None
        return self

    def exec(self):
        t = time.time()
        if self.wait_time == -1 or t - self.last_finish_t < self.wait_time:
            return
        self.last_begin_t = t
        try:
            self.result = self.fun(*self.args)
        except Exception as e:
            self.result = dict(code=500, msg=str(e))
        self.last_finish_t = t

    def __repr__(self):
        return f"result:{self.result}"


class Task(TableBase):

    def __init__(self) -> None:
        self.tasks: List[TaskConfig] = []

    def add_task(self, **kw):
        t = TaskConfig().load(**kw)
        self.tasks.append(t)
        return self

    def load(self, tasks):
        for t in tasks:
            self.add_task(**t)
        return self

    def loop(self):
        for t in self.tasks:
            t.exec()
        return self

    def run(self):
        while True:
            self.loop()
            time.sleep(1)

    def start(self):
        _thread.start_new_thread(self.run, ())


TASK_MANAGER: Dict[str, Task] = dict()


def get_task(name):
    if name not in TASK_MANAGER:
        TASK_MANAGER[name] = Task().set_model(
            TaskConfig().set_resource(f"data/task/{name}.json")
        )
    return TASK_MANAGER[name]
