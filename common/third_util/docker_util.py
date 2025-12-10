from common.tool.export import OsUtil
import docker


class DockerUtil:

    _o: OsUtil = None
    _client: docker.DockerClient = None

    @property
    def o(self):
        if self._o is None:
            self._o = OsUtil("docker")
        return self._o

    @property
    def client(self):
        if self._client is None:
            self._client = docker.from_env()
            self._client.ping()
        return self._client

    def build(self, path, tag="myapp:v1"):
        """
        self.o.set_env(path)

        """

        self.o.run("build", path, "--progress=plain", "-D", "-t", tag)  # "-f", path
        # self.client.images.build(path=path, tag=tag)

    def pull(self, name):
        self.o.run("pull", name)

    def info(self):
        self.o.run("info")
