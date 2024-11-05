from common.util.baseconfig import ConfigBase, DictModel
from common.util.module import Module
import _thread
import time


class TaskConfg(ConfigBase):
    tasks = dict()


class Task:
    PY_MODULE_TYPE = 'py_module'
    PY_FILE_TYPE = ''

    def __init__(self) -> None:
        self.config = dict()

    def set_task(self, task_name, task_type, task_args):
        task_info = self.config.tasks.get(task_name, {})
        task_info["task_type"] = task_type
        task_info["task_args"] = task_args
        self.config.save()
        return self

    def loop(self):
        # for k, v in self.config.tasks.get_value().items():
        #     self.do_task(k, **v)
        return self

    def do_task(self, task_name, task_type, task_args):
        if task_type == self.PY_MODULE_TYPE:
            self.do_py_model_task(task_name, *task_args)
        else:
            raise Exception("gg")

    def do_py_model_task(self, name, path, md_name, func_name, *args):
        fun = Module().load_module(md_name, path, func_name)
        return fun(*args)

    def run(self):
        while True:
            self.loop()
            time.sleep(1)

    def start(self):
        _thread.start_new_thread(self.run, ())
        return self
