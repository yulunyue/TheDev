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

from .task_config import TaskConfig


class Task:
    def __init__(self):
        self.main_thread = Thread(target=self.run, daemon=True)

    def loop(self):
        for t in TaskConfig.all():
            t.exec()
        TaskConfig.save()
        return self

    def run(self):
        while True:
            self.loop()
            time.sleep(1)

    def start(self):
        self.main_thread.start()
        return self

    def add_task(self, name, **kw):
        return TaskConfig.get(name).update(name=name, **kw)


TASK_MANAGE = Task()
