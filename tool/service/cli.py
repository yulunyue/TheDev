from common.tool.export import OsUtil, System, ToolBase
from common.third_util.io.api import Api
from common.util.export import File, logger


class Cli(ToolBase):

    def npm_build(self):
        OsUtil("npm.cmd").set_env("font").run("run", "build")

    def package(self):
        f = File("./")
        f.zip(
            "data/the_dev.zip",
            targets=["font/dist", "common", "app/tool"],
            ignores=[".*__pycache__"],
        )

    def install(self, ip_port):
        api = Api().set_endpoint(f"http://{ip_port}")
        res = api.post_files(f"/app/manage/post_file", "data/the_dev.zip")
        logger.info(res)
        # api.post(f"/app/manage/unzip", data=dict(path="data/upload/the_dev.zip"))

    def restart(self, ip_port, config):
        api = Api().set_endpoint(f"http://{ip_port}")
        res = api.post(f"/app/manage/restart", data=dict(config=config))
        logger.map(res=res)


if __name__ == "__main__":
    Cli().run()
