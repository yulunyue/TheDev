from common.tool.export import ToolBase
from common.util.export import File, logger

from .model import Fp, ROOT, TrajectoryBuilder
from .model.constants import OPENCODE_JSON_FILE_NAME
from .service import FeishuSync, TaskBuilder, TaskPackager
from .service.task_packager import OUTPUT_DIR

STEPS = [
    "docker_build",
    "pre_check",
    "llm_build",
    "llm_check",
    "package",
    "quality_check",
    "feishu_sync",
]

_ERROR_MAX_LEN = 500


class ZbTool(ToolBase):
    def __init__(self):
        self.builder = TaskBuilder()
        self.packager = TaskPackager()
        self.trajectory_builder = TrajectoryBuilder()

    def run(self, name, manual=False):
        self.builder.set_env(name)
        opencode_json = self.builder.src_root.child(OPENCODE_JSON_FILE_NAME)

        step_data = opencode_json.read_file() if opencode_json.exists() else {}
        completed_step = step_data.get("step")
        start_index = 0
        if completed_step and completed_step in STEPS:
            start_index = STEPS.index(completed_step) + 1

        if start_index >= len(STEPS):
            logger.info(f"[{name}] 全部步骤已完成")
            return

        for i in range(start_index, len(STEPS)):
            step = STEPS[i]
            try:
                logger.info(f"[{name}] 开始执行: {step}")
                self._exec_step(step, name, manual)
                step_data = opencode_json.read_file() if opencode_json.exists() else {}
                step_data["step"] = step
                opencode_json.write_file(step_data)
                logger.info(f"[{name}] 完成: {step}")
            except Exception as e:
                step_data = opencode_json.read_file() if opencode_json.exists() else {}
                step_data["step"] = step
                step_data["error"] = str(e)[:_ERROR_MAX_LEN]
                opencode_json.write_file(step_data)
                logger.error(f"[{name}] 失败: {step}, 原因: {str(e)[:_ERROR_MAX_LEN]}")
                raise

    def _exec_step(self, step, name, manual):
        if step == "docker_build":
            self.builder.docker_build()
        elif step == "pre_check":
            self.builder.pre_check()
        elif step == "llm_build":
            self.builder.llm_build(manual=manual)
        elif step == "llm_check":
            self.builder.llm_check()
        elif step == "package":
            self._do_package(name)
        elif step == "quality_check":
            self._do_quality_check(name)
        elif step == "feishu_sync":
            FeishuSync().sync(name)

    def _do_package(self, name):
        root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        instance_json = root.child(f"{root.name}.json")
        self.packager.fix_files(root)
        self.trajectory_builder.build_from_root(root)
        self.packager.package(root, instance_json)

    def _do_quality_check(self, name):
        from pathlib import Path as StdPath

        from .check import quality_check
        from .check.quality_check import run_checks

        root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        env = root.name.split("-")[0]
        pr_id = root.name.split("-")[-1]
        image_name = f"{env}:{pr_id}"

        zip_file = OUTPUT_DIR.child(f"{root.name}.zip")
        project_dir = OUTPUT_DIR.child(root.name)

        if not project_dir.exists() and zip_file.exists():
            zip_file.unzip(dst=project_dir)

        report_path = root.child(f"{root.name}_qc_report.json").path
        quality_check.SAVE_JSON_REPORT = True
        passed = run_checks(
            StdPath(project_dir.get_abs_path()), image_name, report_path
        )
        quality_check.SAVE_JSON_REPORT = False
        if not passed:
            raise Exception("quality_check 未通过")

    def llm_build(self, name, manual=False):
        self.builder.set_env(name).llm_build(manual=manual)

    def docker_build(self, name):
        self.builder.set_env(name).docker_build()

    def pre_check(self, name):
        self.builder.set_env(name).pre_check()

    def llm_check(self, name):
        self.builder.set_env(name).llm_check()

    def package(self, name):
        self._do_package(name)


if __name__ == "__main__":
    ToolBase.run(ZbTool())
