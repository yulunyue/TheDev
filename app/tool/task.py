from common.tool.export import get_task


class TaskTool:

    def start(self):
        s = get_task().start()
        return s.source.to_web_view()

    def query(self, **kw):
        return get_task().source.to_web_view()
