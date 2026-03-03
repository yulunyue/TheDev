from common.tool.export import OsUtil, System, ToolBase
from common.third_util.io.api import Api
from common.util.export import File

CONFIG = File("config/setting/dev.json").read_file()


class Cli(ToolBase):
    def restart(self):
        pid = System.get_pid_by_port(10000)
        OsUtil("kill").run("-9", pid)
        OsUtil("python").system("main.py", "http", "2>&1", "&")

    def build_font(self):
        OsUtil("npm.cmd").set_env("font").run("run", "build")

    def build_all(self):
        f = File("./")
        f.zip(
            "data/the_dev.zip",
            targets=["font/dist", "common", "app/tool"],
        )

    def build(self):
        self.build_font()
        self.build_all()
        self.upload()

    def upload(self):
        uri = f"http://{CONFIG['ip']}:{CONFIG['port']}"
        api = Api()
        api.post_files(f"{uri}/app/api/post_file", "data/the_dev.zip")
        api.post(f"{uri}/app/util/restart", data=dict(path="data/upload/the_dev.zip"))


if __name__ == "__main__":
    Cli().run()
