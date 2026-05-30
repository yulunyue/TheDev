from common.tool.export import ToolBase
from common.util.export import File

from .model import Fp, ROOT, TrajectoryBuilder
from .service import TaskBuilder, TaskPackager


class ZbTool(ToolBase):
    def __init__(self):
        self.builder = TaskBuilder()
        self.packager = TaskPackager()
        self.trajectory_builder = TrajectoryBuilder()

    def llm_build(self, name, manual=False):
        self.builder.set_env(name).llm_build(manual=manual)

    def docker_build(self, name):
        self.builder.set_env(name).docker_build()

    def pre_check(self, name):
        self.builder.set_env(name).pre_check()

    def llm_check(self, name):
        self.builder.set_env(name).llm_check()

    def package(self, name):
        root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        instance_json = root.child(f"{root.name}.json")
        self.packager.fix_files(root)
        self.trajectory_builder.build_from_root(root)
        self.packager.package(root, instance_json)


if __name__ == "__main__":
    ZbTool().run()
