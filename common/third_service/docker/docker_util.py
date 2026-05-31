from common.tool.export import OsUtil
from common.util.export import List, Optional


class DockerUtil(OsUtil):
    def __init__(self, error_exit_flag=True):
        super().__init__("docker", error_exit_flag=error_exit_flag)

    def ps(self, all=False, filters: Optional[List[str]] = None):
        args = ["ps"]
        if all:
            args.append("-a")
        if filters:
            for f in filters:
                args.extend(["--filter", f])
        return self.run(*args)

    def images(self, name: Optional[str] = None):
        args = ["images"]
        if name:
            args.append(name)
        return self.run(*args)

    def pull(self, image: str):
        return self.run("pull", image)

    def run_container(
        self,
        image: str,
        name: Optional[str] = None,
        detach=True,
        rm=False,
        ports: Optional[dict] = None,
        volumes: Optional[dict] = None,
        env: Optional[dict] = None,
        network: Optional[str] = None,
        cmd: Optional[str] = None,
    ):
        args = ["run"]
        if detach:
            args.append("-d")
        if rm:
            args.append("--rm")
        if name:
            args.extend(["--name", name])
        if ports:
            for host_port, container_port in ports.items():
                args.extend(["-p", f"{host_port}:{container_port}"])
        if volumes:
            for host_path, container_path in volumes.items():
                args.extend(["-v", f"{host_path}:{container_path}"])
        if env:
            for k, v in env.items():
                args.extend(["-e", f"{k}={v}"])
        if network:
            args.extend(["--network", network])
        args.append(image)
        if cmd:
            if any(c in cmd for c in "|;&$><()'"):
                args.extend(["sh", "-c", cmd])
            else:
                args.extend(cmd.split())
        return self.run(*args)

    def stop(self, container: str):
        return self.run("stop", container)

    def rm(self, container: str, force=False):
        args = ["rm"]
        if force:
            args.append("-f")
        args.append(container)
        return self.run(*args)

    def exec_run(self, container: str, cmd_str: str, interactive=False):
        args = ["exec"]
        if interactive:
            args.append("-it")
        args.extend([container, "sh", "-c", cmd_str])
        return self.run(*args)

    def logs(self, container: str, tail: Optional[int] = None, follow=False):
        args = ["logs"]
        if follow:
            args.append("-f")
        if tail is not None:
            args.extend(["--tail", str(tail)])
        args.append(container)
        return self.run(*args)

    def compose(self, *args, file: Optional[str] = None, project: Optional[str] = None):
        cmd_args = ["compose"]
        if file:
            cmd_args.extend(["-f", file])
        if project:
            cmd_args.extend(["-p", project])
        cmd_args.extend(args)
        return self.run(*cmd_args)

    def compose_up(
        self, file: Optional[str] = None, project: Optional[str] = None, detach=True
    ):
        args = ["up"]
        if detach:
            args.append("-d")
        return self.compose(*args, file=file, project=project)

    def compose_down(self, file: Optional[str] = None, project: Optional[str] = None):
        return self.compose("down", file=file, project=project)

    def build(self, tag: str, path=".", file: Optional[str] = None, network: Optional[str] = None):
        args = ["build", "-t", tag]
        if file:
            args.extend(["-f", file])
        if network:
            args.extend(["--network", network])
        args.append(path)
        return self.run(*args)

    def inspect(self, name: str):
        return self.run("inspect", name)

    def network_create(self, name: str, driver: Optional[str] = None):
        args = ["network", "create"]
        if driver:
            args.extend(["--driver", driver])
        args.append(name)
        return self.run(*args)

    def volume_create(self, name: str):
        return self.run("volume", "create", name)

    def login(
        self, registry: Optional[str] = None, username: str = None, password: str = None
    ):
        args = ["login"]
        if registry:
            args.append(registry)
        if username:
            args.extend(["-u", username])
        if password:
            args.extend(["-p", password])
        return self.run(*args)

    def tag(self, source: str, target: str):
        return self.run("tag", source, target)

    def push(self, image: str):
        return self.run("push", image)
