from common.util.export import logger, File
from app.yly.zb.manage import ZbMangae, CS, query_one, query_task
from common.tool.export import ToolBase


class ZbTool(ToolBase):
    def __init__(self):
        self.z = ZbMangae()

    def view(self):
        self.z.view()

    def submit(self):
        self.z.submit()

    def task_update(self):
        self.z.task_update()

    def run_all(self, key=""):
        self.z.run_all(key)

    def error(self, key):
        [d.set_error_msg(CS.ERROR) for d in query_task(key)]

    def run_one(self, key):
        self.z.run_one(key)

    def show_pre(self, key):
        self.z.show_all(key, "pre")

    def show_test(self, key):
        self.z.show_all(key, "test")

    def show_code(self, key):
        self.z.show_all(key, "code")

    def query_log(self, key="log"):
        query_file = File(f"data/zb/query/{key}.json").write_if_not_exists(
            dict(
                key=f".*" + CS.FAILED + ".*",
                search_key="",
                log_name="docker.log",
                util="",
            )
        )
        self.z.query_log(**query_file.read_file())
        logger.info(query_file)


if __name__ == "__main__":
    ZbTool().run()
