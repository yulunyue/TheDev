from .task_base import ZbTask, REPO_BASE, CS, logger
import time
from common.util.export import get_dev_log


def get_volumn_v(kw):
    return " ".join([f"-v {k}:{v}" for k, v in kw.items()])


class DockerTask(ZbTask):
    def set_env(self, docker_image_name, remote_ip, log_flie):
        from common.third_util.docker_util import DockerUtil

        self.docker_image_name = docker_image_name
        self.dock_util = DockerUtil(
            docker_image_name,
            log_file=log_flie,
            remote_ip=remote_ip,
        )

        return self

    def docker_build(self):
        if not self.dock_util.build(self.input_dir.get_abs_path()):
            self.local_cfg.set_error_msg(CS.FAILED, CS.DOCKER_BUILD_FAILED)
            return False
        return True

    def get_volumn_v(self, kw=None):
        return get_volumn_v(self.get_volumn(kw))

    def get_volumn(self, kw=None):
        ret = {
            self.local_cfg.code_patch.f.get_abs_path(): f"{REPO_BASE}/{self.local_cfg.code_patch.f.file_name}",
            self.local_cfg.test_patch.f.get_abs_path(): f"{REPO_BASE}/{self.local_cfg.test_patch.f.file_name}",
            self.main_py_file.get_abs_path(): f"{REPO_BASE}/{self.main_py_file.file_name}",
            # self.local_cfg.py_test_result_json.get_abs_path(): f"/testbed_output/{CS.RESULT_JSON_FILE}",
            self.input_dir.get_abs_path(): f"/testbed_output",
            # self.local_repo.get_abs_path(): self.local_repo.path,
        }
        if kw:
            ret.update(kw)
        return ret

    def play(self):
        result_files = [
            "results.json",
            "pre.log",
            "pre.json",
            "test.json",
            "code.json",
            "test.log",
            "code.log",
        ]
        for f in result_files:
            self.input_dir.child(f).remove()
        if not self.docker_build():
            return
        self.local_cfg.py_test_result_json.remove()
        logger.info(
            f"\ndocker run -p 5678:5678 {self.get_volumn_v()} -it {self.docker_image_name}\n"
        )
        status, msg = self.dock_util.run(
            ";".join(
                [
                    "/bin/bash -i -c 'cd /testbed && python run_verification.py",
                ]
                + [f"cp -f {f} /testbed_output/{f}" for f in result_files]
            )
            + "'",
            self.get_volumn(),
            REPO_BASE,
            env={"INSTANCE_ID": self.local_cfg.cg.instance_id.get_value()},
        )

        self.logger.debug(msg)
        self.print_result()
