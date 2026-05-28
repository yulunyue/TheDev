from common.tool.export import ToolBase
from common.util.export import File

from .model import Fp, ROOT, TrajectoryBuilder
from .service import TaskBuilder, TaskPackager


class ZbTool(ToolBase):
    def __init__(self):
        self.builder = TaskBuilder()
        self.packager = TaskPackager()
        self.trajectory_builder = TrajectoryBuilder()

    def build(self, name):
        root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        self.builder.build(root)

    def build_docker(self, name, proxy_host=None):
        self.builder.build_docker(name, proxy_host)

    def package(self, name):
        root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        instance_json = root.child(f"{root.name}.json")
        self.trajectory_builder.build_from_root(root)
        self.packager.package(root, instance_json)


if __name__ == "__main__":
    ZbTool().run()