from common.tool.export import OsUtil


class DockerUtil:
    def __init__(self):
        self.o = OsUtil("docker")

    def build(self, path, name="myapp:v1"):
        self.o.set_env(path)
        self.o.run("build", "--progress=plain", "-D", "-t", name, ".")  # "-f", path

    def pull(self, name):
        self.o.run("pull", name)

    def info(self):
        self.o.run("info")
