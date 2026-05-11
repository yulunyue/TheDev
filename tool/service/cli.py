from common.tool.export import OsUtil, System, ToolBase, GC
from common.third_util.io.api import Api
from common.util.export import File, logger, time, md5
import random

THE_DEV_ZIP_PATH = "data/the_dev.zip"
UPLOAD_ZIP_PATH = "data/upload/the_dev.zip"


class Cli(ToolBase):
    def load(self, name="Api", ip_port="", b64_pkg_num=8192 * 4):
        self.api = Api(name).set_endpoint(f"http://{ip_port}")
        self.b64_pkg_num = b64_pkg_num

    def npm_build(self):
        File("font/dist").remove()
        OsUtil(GC.npm_path.get_value()).set_env("font").run("run", "build")

    def package(self):
        f = File("./")
        f.zip(
            THE_DEV_ZIP_PATH,
            targets=["font/dist", "common", "app/tool", "tool", "main.py"],
            ignores=[".*__pycache__"],
        )
        logger.info("package")

    def upload(self):
        self.api.post_files(f"/app/manage/post_file", THE_DEV_ZIP_PATH)

    def upload_base_64(self):
        data = File(THE_DEV_ZIP_PATH).read_b64_data()
        all_num = len(data) // self.b64_pkg_num
        for idx in range(0, all_num + 1):
            res = self.api.post(
                f"/app/manage/post_files_base64",
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
            # time.sleep(random.randint(2, 7))
        logger.map(all_size=len(data), md5_check=md5(data))

    def install(self):
        res = self.api.post(f"/app/manage/unzip", data=dict(path=UPLOAD_ZIP_PATH))
        logger.map(res=res)

    def restart(self, config):
        res = self.api.post(f"/app/manage/restart", data=dict(config=config))
        logger.map(res=res)

    def cicd(self, config):
        self.npm_build()
        self.package()
        self.upload_base_64()
        self.install()
        self.restart(config)


if __name__ == "__main__":
    Api.enable_globel_log()
    Cli().run()
