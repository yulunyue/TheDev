from common.util.export import Module, get_log, THE_DEV_CONSTANT
from common.tool.base_class.table_base import (
    TableBase,
    StrModel,
    NumberModel,
    ConfigBase,
    TableConfig,
    DictModel,
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
        self.wait_time = NumberModel(default_value=1)
        self.last_begin_t = NumberModel(default_value=0)
        self.last_finish_t = NumberModel(default_value=0)
        self.result = DictModel()
        super().__init__()

    def load(self, **kw):
        super().load(**kw)
        self.fun = Module().load_module(
            self.module_name.get_value(),
            self.root_path.get_value(),
            self.fun_name.get_value(),
        )
        return self

    def exec(self):
        now_t = time.time()
        if (
            self.wait_time.get_value() == -1
            or now_t - self.last_finish_t.get_value() < self.wait_time.get_value()
        ):
            return
        self.last_begin_t.set_value(now_t)
        try:
            self.result.update(
                code=THE_DEV_CONSTANT.CODE_200,
                value=self.fun(*self.args.get_value().split(",")),
            )
        except Exception as e:
            self.result.update(code=THE_DEV_CONSTANT.CODE_500, value=str(e))
        self.last_finish_t.set_value(time.time())

    def __repr__(self):
        return f"result:{self.result}"


class Task(TableBase):
    body: List[TaskConfig]

    def loop(self):
        for t in self.body:
            t.exec()
        return self

    def run(self):
        while True:
            self.loop()
            time.sleep(60)

    def start(self):
        _thread.start_new_thread(self.run, ())
        return self


TASK_MANAGER: Dict[str, Task] = dict()


def get_task(name):
    if name not in TASK_MANAGER:
        TASK_MANAGER[name] = Task().set_model(
            TaskConfig().set_resource(f"data/task/{name}.json")
        )
    return TASK_MANAGER[name]
