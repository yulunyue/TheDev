from common.util.export import logger, File
from common.tool.export import ConfigBase, StrModel
from obs import ObsClient


class ObsConfig(ConfigBase):
    ak = StrModel()
    sk = StrModel()
    endpoint = StrModel()
    bucket = StrModel()


class ObsUtil:
    def __init__(self, name):
        self.config = ObsConfig(name).set_resource(f"obs_{name}")
        self._obs_client: ObsClient = None

    @property
    def obs_client(self):
        if self._obs_client is None:
            try:
                self._obs_client = ObsClient(
                    access_key_id=self.config.ak.get_value(),
                    secret_access_key=self.config.sk.get_value(),
                    server=self.config.endpoint.get_value(),
                )
            except Exception as e:
                raise Exception(e)
        return self._obs_client

    def download(self, remote_path: str, down_load_path: str):
        res = self.obs_client.downloadFile(
            self.bucket_name, remote_path, downloadFile=down_load_path
        )
        return res

    def list_buckets(self):
        r = self.obs_client.listBuckets()
        ret = [d["name"] for d in r["body"]["buckets"]]
        logger.info(ret)
        return ret

    def list_dir(self, prefix=""):
        ret = self.obs_client.listObjects(self.config.bucket.get_value(), prefix)
        return [[v["key"], v["lastModified"]] for v in ret["body"]["contents"]]

    def upload(self, f: File):
        if isinstance(f, str):
            f = File.new(f)
        if f.is_dir():
            f = f.zip()
        res = self.obs_client.uploadFile(
            self.config.bucket.get_value(), f.file_name, f.get_abs_path()
        )
        obj_uri = res["body"]["objectUrl"]
        logger.info(f"wget {obj_uri} -O {f.file_name}")

    def check(self):
        pass


if __name__ == "__main__":
    args, kw = sys_argc_parse()
    print(args, kw)
    print(getattr(ObsUtil(**kw), args[0])(*args[1:]))
