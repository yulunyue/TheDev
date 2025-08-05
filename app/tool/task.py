from common.tool.export import get_task


class TaskTool:
    T = get_task("taskconfig").start()

    def query(self, **kw):
        return
