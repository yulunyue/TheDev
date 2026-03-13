from common.tool.export import Task, get_task, TASK_MANAGER, ToolBase


class TaskTool(ToolBase):
    def loop(self):
        t = get_task()
        t.loop()
        t.source.save()

    def run_task(self, name="cargo_c4", **kw):
        t = get_task()
        t.source.get(name).exec()
        t.source.save()


if __name__ == "__main__":
    TaskTool().run()
