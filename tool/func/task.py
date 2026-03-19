from common.tool.export import T, ToolBase


class TaskTool(ToolBase):
    def loop(self):
        T.loop()

    def run_task(self, name="cargo_c4", **kw):
        t = get_task()
        t.source.get(name).exec()
        t.source.save()


if __name__ == "__main__":
    TaskTool().run()
