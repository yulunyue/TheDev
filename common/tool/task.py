from common.util.export import Module, get_log

logger = get_log("task")
import _thread
import time
from typing import Dict, List


class TaskConfig:

    def load(self, module_name, fun_name, root_path, args=None, wait_time=-1):
        self.wait_time = wait_time
        self.module_name = module_name
        self.fun_name = fun_name
        self.args = args or []
        self.root_path = root_path
        self.fun = Module().load_module(module_name, root_path, fun_name)
        self.last_begin_t = 0
        self.last_finish_t = 0
        return self

    @property
    def key(self):
        return self.module_name + self.fun_name

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
        logger.info(f"{self.key}:{self.args}{self.result}")


class Task:

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


TASK_MANAGER = Task()
