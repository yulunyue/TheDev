from common.tool.export import OsUtil
import docker
from common.util.export import logger


class DockerUtil:

    _o: OsUtil = None
    _client: docker.DockerClient = None

    def __init__(self, image_name):
        self.image_name = image_name

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

    def check_image_exists(self):
        try:
            self.client.images.get(self.image_name)
            return True
        except Exception as e:
            return False

    def build(self, path):
        """
        self.o.set_env(path)

        """

        self.o.run(
            "build", path, "--progress=plain", "-D", "-t", self.image_name
        )  # "-f", path
        # self.client.images.build(path=path, tag=tag)

    def pull(self, name):
        self.o.run("pull", name)

    def info(self):
        self.o.run("info")

    def get_volumes(self, env):
        if env is None:
            return dict()
        ret = dict()
        for k, v in env.items():
            if isinstance(v, str):
                ret[k] = dict(bind=v, mode="rw")
            else:
                ret[k] = v
        return ret

    def run(self, command, volumes, working_dir, env: dict = None):
        exit_code = 1
        msgs = ""
        volumes = self.get_volumes(volumes)
        try:
            logger.debug(
                f"   -> 启动容器 (镜像: {self.image_name}). volumes:{volumes}, env:{env}.."
            )

            container = self.client.containers.run(
                self.image_name,
                command=command,
                volumes=volumes,
                network_mode="none",
                environment=env or dict(),
                remove=True,
                detach=True,
                # 建议加上 tty=True，防止 bash 抱怨没有终端
                tty=True,
                working_dir=working_dir,
            )
            # 流式日志
            for chunk in container.logs(stream=True, follow=True):
                msgs += chunk.decode("utf-8", "replace")
            ret = container.wait()
            exit_code = ret.get("StatusCode", 1)
        except docker.errors.ContainerError as e:
            logger.debug(f"   -> ❌ 错误: 容器运行异常退出")
            logger.debug(f"   -> 退出码: {e.exit_status}")
            logger.debug(f"   -> 错误详情: {str(e)}")

        except Exception as e:
            logger.exception(f"   -> ❌ 运行容器时发生未知错误: {e}", stacklevel=True)
        return exit_code, msgs
