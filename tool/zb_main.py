from common.util.export import ToolBase, logger
from app.yly.zb.manage import ZbMangae, CS


class ZbTool(ToolBase):
    def prepare(self, *args):
        self.z = ZbMangae()
        return super().prepare(*args)

    def view(self):
        self.z.view()

    def task_update(self):
        self.z.task_update()

    def exec(self, key=""):
        self.z.exec(key)


if __name__ == "__main__":
    ZbTool().run()
