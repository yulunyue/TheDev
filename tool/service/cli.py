from common.tool.export import OsUtil, System, ToolBase
from common.third_util.io.api import Api
from common.util.export import File


class Cli(ToolBase):

    def npm_build(self):
        OsUtil("npm").set_env("font").run("run", "build")

    def package(self):
        f = File("./")
        f.zip(
            "data/the_dev.zip",
            targets=["font/dist", "common", "app/tool"],
            ignores=[".*__pycache__"],
        )

    def install(self, ip_port):
        api = Api().set_endpoint(f"http://{ip_port}")
        api.post_files(f"/app/manage/post_file", "data/the_dev.zip")
        api.post(f"/app/manage/unzip", data=dict(path="data/upload/the_dev.zip"))

    def restart(self, ip_port, config):
        api = Api().set_endpoint(f"http://{ip_port}")
        api.post(f"/app/manage/restart", data=dict(config=config))


if __name__ == "__main__":
    Cli().run()
