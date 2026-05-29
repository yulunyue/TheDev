import re
from common.third_util.llm.opencode_client import OpencodeClient, logger
from common.util.export import File
from common.third_service.docker.docker_util import DockerUtil

from ..model.constants import Fp, ROOT, get_promot, REPO_ROOT


class TaskBuilder:
    def __init__(self, opencode_client=None):
        self.client = opencode_client or OpencodeClient

    def set_env(self, name: str):
        self.src_root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        self.name = self.src_root.name
        self.env = self.name.split("-")[0]
        self.src_test_pattch = self.src_root.child(Fp.test_patch)
        self.tmp_root = (
            File(f"data/tmp/docker_build/{self.name}")
            .remove()
            .make_dir_if_not_exist(is_dir=True)
        )
        self.src_final_diff = self.src_root.child(Fp.final_diff)
        self.instance_json = self.src_root.child(f"{self.src_root.name}.json")
        self.repo_root = REPO_ROOT.child(self.env)
        return self

    @property
    def base_commit(self):
        return self.instance_json.get("base_commit")

    @property
    def issue_url(self):
        return self.instance_json.get("issue_url")

    def llm(self):
        o = self.client.new(
            self.repo_root.path, "http://127.0.0.1:45799"
        ).start_server()
        promot = get_promot(
            self.base_commit,
            self.issue_url,
            self.src_test_pattch.read_file(),
            self.src_final_diff,
        )
        result = o.do_prompt(promot)
        o.stop()
        session_id = result.data["session_id"]
        self.tmp_root.child(".opencode_session_id").write_file(session_id)
        logger.info(f"session_id={session_id}")
        return result

    def build(self):
        self.mock_root = File(f"app/zb/mock/{self.env}").make_dir_if_not_exist(True)
        image_name = self.env
        self._docker_build(self.tmp_root, image_name)
        logger.info(f"Docker build completed: {image_name}")
        return image_name

    def _copy_task_files(self, files_to_copy):
        for f in files_to_copy:
            src_file = self.src_root.child(f)
            mock_file = self.mock_root.child(f)
            dst_file = self.tmp_root.child(f)
            mock_data = "" if not mock_file.exists() else mock_file.read_file()
            data = self.hander_file(f, src_file.read_file(), mock_data)
            dst_file.write_file(data)

    def hander_file(self, file_name, src, mock):
        if mock:
            return mock
        return src

    def _patch_setup_repo(self, dst_file: File):
        instance_json = self.src_root.child(f"{self.src_root.name}.json")
        config = instance_json.read_file()
        base_commit = config.get("base_commit", "")

        src_setup_repo = self.src_root.child(Fp.setup_repo_sh)
        extra_deps = (
            self._extract_deps(src_setup_repo) if src_setup_repo.exists() else ""
        )

        mock_setup_repo = self.mock_root.child(Fp.setup_repo_sh)
        template = mock_setup_repo.read_file()

        content = template.replace("{{base_commit}}", base_commit)
        if extra_deps:
            content = content.replace("{{extra_deps}}", extra_deps)
        else:
            content = content.replace("{{extra_deps}}", "")

        dst_file.write_file(content)

    def _extract_deps(self, setup_repo: File) -> str:
        content = setup_repo.read_file()
        uv_match = re.search(r"uv pip install\s+([^\s]+(?:\s+[^\s]+)*?)\s+-e", content)
        if uv_match:
            deps_str = uv_match.group(1)
            deps = [d.strip('"') for d in deps_str.split() if not d.startswith("-e")]
            return " ".join(f'"{d}"' for d in deps if d)
        pip_match = re.search(r"pip install\s+([^\s]+(?:\s+[^\s]+)*?)", content)
        if pip_match:
            deps_str = pip_match.group(1)
            deps = [d.strip('"') for d in deps_str.split()]
            return " ".join(f'"{d}"' for d in deps if d)
        return ""

    def _docker_build(self, tmp_root: File, image_name: str):
        logger.info(f"Running: docker build -t {image_name}")
        self._copy_task_files(Fp.docker_build())
        DockerUtil().build(image_name, tmp_root.get_abs_path())
        logger.info(f"Docker build success: {image_name}")

    def check(self, fps):
        self._copy_task_files(fps)
        image_name = self.env
        abs_path = self.tmp_root.get_abs_path()

        DockerUtil().run_container(
            image=image_name,
            detach=False,
            rm=True,
            network="none",
            volumes={abs_path: "/testbed/verification"},
            cmd="python /testbed/verification/run_verification.py",
        )

        results_json = self.tmp_root.child("results.json")
        if results_json.exists():
            return results_json.read_file()
        return None

    def pre_check(self):
        self.check(
            [
                Fp.code_patch,
                Fp.run_verification_py,
                Fp.test_patch,
            ]
        )

    def llm_check(self):
        self.check(
            [
                Fp.final_diff,
                Fp.run_verification_py,
                Fp.test_patch,
            ]
        )
