from common.util.export import ToolBase
from common.third_util.docker_util import DockerUtil
from common.util.export import logger


class DockerCli(ToolBase):
    def prepare(self, *args):
        self.u = DockerUtil()

    def build(self, path):
        self.u.build(path)

    def info(self, **kw):
        logger.info(self.u.info())


if __name__ == "__main__":
    DockerCli().run()
