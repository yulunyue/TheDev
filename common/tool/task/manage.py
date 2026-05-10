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
    Type,
    IO_MANAGE,
    C,
)
from .task_config import TaskConfig


class Task:
    model: Type[TaskConfig] = TaskConfig

    def set_resource(self, path):
        self.model.set_resource(path)
        return self

    def loop(self):
        for t in self.model.all():
            t.exec()
        return self

    def run(self):
        time.sleep(3)
        while True:
            self.loop()
            time.sleep(1)

    def start(self):
        self.main_thread = Thread(target=self.run, daemon=True)
        self.main_thread.start()
        return self

    def add_task(self, name, **kw):
        return self.model.get(name).update(name=name, **kw)


TASK_MANAGE = Task()
