from common.tool.export import OsUtil
import docker
from common.util.export import logger, os


class DockerUtil:

    _o: OsUtil = None
    _client: docker.DockerClient = None

    def __init__(self, image_name="base"):
        self.image_name = image_name
        self.remote_ip = None  # "tcp://192.168.1.6:2375"

    @property
    def o(self):
        if self._o is None:
            self._o = OsUtil("docker")
        return self._o

    @property
    def client(self):
        if self._client is None:
            if self.remote_ip:
                self._client = docker.DockerClient(base_url=self.remote_ip, timeout=10)
            else:
                self._client = docker.from_env()
            self._client.ping()
        return self._client

    def check_image_exists(self):
        try:
            self.client.images.get(self.image_name)
            return True
        except Exception as e:
            return False

    def build(self, path, from_image_name):
        if not self.check_image_exists():
            self.tag(from_image_name, self.image_name)
        if self.image_name.split(":").pop().startswith("v"):
            self.re_build(path)

    def re_build(self, path):
        self.o.run(
            "build", path, "--progress=plain", "-D", "-t", self.image_name
        )  # "-f", path

    def tag(self, from_name, to_image_name):
        self.o.run(f"tag", from_name, to_image_name)

    def pull(self, name):
        self.o.run("pull", name)

    def info(self):
        return self.client.info()

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
        """
        docker run -v d:/thebug/TheDev:/TheDev -it zb:latest
        """
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
                msgs += chunk.decode("utf-8", errors="ignore")
            ret = container.wait()
            exit_code = ret.get("StatusCode", 1)
        except docker.errors.ContainerError as e:
            logger.debug(f"   -> ❌ 错误: 容器运行异常退出")
            logger.debug(f"   -> 退出码: {e.exit_status}")
            logger.debug(f"   -> 错误详情: {str(e)}")

        except Exception as e:
            logger.exception(f"   -> ❌ 运行容器时发生未知错误: {e}", stacklevel=True)
        return exit_code, "\n".join(
            [v for v in msgs.replace("\r\n", "\n").split("\n") if v]
        )
