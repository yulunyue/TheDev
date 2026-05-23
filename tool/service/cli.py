from common.tool.export import OsUtil, ToolBase, GC, ProcessLock, System
from common.third_util.io.api import Api
from common.third_util.io.api_config import API_CONFIG
from common.util.export import File, logger, md5

THE_DEV_ZIP_PATH = "data/the_dev.zip"
UPLOAD_ZIP_PATH = "data/upload/the_dev.zip"


class Cli(ToolBase):
    def _load(self, server="bolun"):
        cfg = API_CONFIG.get(server)
        self.api = Api("Api").set_endpoint(f"http://{cfg.endpoint.get_value()}")

    def npm_build(self):
        File("font/dist").remove()
        OsUtil(GC.npm_path.get_value()).set_env("font").run("run", "build")

    def package(self):
        f = File("./")
        f.zip(
            THE_DEV_ZIP_PATH,
            targets=[
                "font/dist",
                "common",
                "app/tool",
                "app/yly",
                "tool",
                "main.py",
                "config/setting/production.json",
            ],
            ignores=[".*__pycache__"],
        )
        logger.info("package")

    def upload(self, server="bolun"):
        self._load(server)
        self.api.post_files(f"/app/manage/post_file", THE_DEV_ZIP_PATH)

    def upload_base_64(self, server="bolun", b64_pkg_num=8192 * 4):
        self._load(server)
        self.b64_pkg_num = b64_pkg_num
        data = File(THE_DEV_ZIP_PATH).read_b64_data()
        all_num = len(data) // self.b64_pkg_num
        for idx in range(0, all_num + 1):
            res = self.api.post(
                "/app/manage/post_files_base64",
                dict(
                    path=UPLOAD_ZIP_PATH,
                    data=data[idx * self.b64_pkg_num : (idx + 1) * self.b64_pkg_num],
                    cur_idx=idx,
                    last_idx=all_num,
                ),
            )
            logger.map(idx=idx, res=str(res)[:200], all_num=all_num)
            if isinstance(res, bytes) and res.startswith(b"<!doctype ht"):
                raise Exception(idx, res[:100], len(data))
        logger.map(all_size=len(data), md5_check=md5(data))

    def _unzip(self, server="bolun"):
        self._load(server)
        res = self.api.post("/app/manage/unzip", data=dict(path=UPLOAD_ZIP_PATH))
        logger.map(res=res)

    def install(self, server="bolun"):
        self.package()
        self._load(server)
        self.api.post_files(f"/app/manage/post_file", THE_DEV_ZIP_PATH)
        res = self.api.post("/app/manage/unzip", data=dict(path=UPLOAD_ZIP_PATH))
        logger.map(res=res)

    def restart(self, server="bolun", config="production"):
        self._load(server)
        res = self.api.post("/app/manage/restart", data=dict(config=config))
        logger.map(res=res)

    def cicd(self, server="bolun", config="production"):
        self.npm_build()
        self.install(server)
        self.restart(server, config)

    def dev(self):
        System.run(["python", "main.py", "dev"])


if __name__ == "__main__":
    Cli().run()
