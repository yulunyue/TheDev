from common.util.export import Module, get_log, THE_DEV_CONSTANT
from common.tool.base_class.table_base import (
    TableBase,
    StrModel,
    NumberModel,
    ConfigBase,
    TableConfig,
    DictModel,
)
import traceback
import _thread
import time
from typing import Dict, List


class TaskConfig(TableConfig):
    module_name = StrModel()
    fun_name = StrModel()
    root_path = StrModel()
    args = StrModel()
    wait_time = NumberModel(default_value=1)
    last_begin_t = NumberModel(default_value=0)
    last_finish_t = NumberModel(default_value=0)
    result = DictModel()
    _fun = None

    def get_call(self):
        if self._fun:
            return self._fun
        self._fun = Module().load_module(
            self.module_name.get_value(),
            self.root_path.get_value(),
            self.fun_name.get_value(),
        )
        return self._fun

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
                value=self.get_call()(*self.args.get_value().split(",")),
            )
        except Exception as e:
            self.result.update(
                code=THE_DEV_CONSTANT.CODE_500, value=traceback.format_exc().split("\n")
            )
        self.last_finish_t.set_value(time.time())

    def __repr__(self):
        return f"result:{self.result}"


class Task:
    def __init__(self, name):
        self.source = TableBase[TaskConfig]().set_resource(name)

    def loop(self):
        for t in self.source.filter():
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


def get_task(name="taskconfig") -> Task:
    if name not in TASK_MANAGER:
        TASK_MANAGER[name] = Task(name)
    return TASK_MANAGER[name]
