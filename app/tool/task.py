from common.tool.export import get_task

PATH = "data/task/taskconfig.json"


class TaskTool:
    def query(self, **kw):
        return get_task(PATH)
