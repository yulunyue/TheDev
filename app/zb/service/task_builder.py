import re
from common.third_util.llm.opencode_client import OpencodeClient, logger
from common.util.export import File
from common.third_service.docker.docker_util import DockerUtil
from common.third_service.git_tool.git_util import GitUtil

from ..model.constants import Fp, ROOT, get_promot, fetch_github_issue, REPO_ROOT


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

    def llm_build(self, manual=False):
        git = GitUtil(workdir=self.repo_root.path)
        git.git_clean()
        git.git_reset(self.base_commit)
        git.git_apply(self.src_test_pattch.path)
        logger.info(f"Git reset to {self.base_commit}, applied test.patch {self.repo_root}")
        
        issue_content = fetch_github_issue(self.issue_url)
        
        promot = get_promot(
            self.issue_url,
            issue_content=issue_content,
            fail_to_pass=self.instance_json.get("FAIL_TO_PASS"),
        )
        logger.info(self.src_root.child(Fp.promot_txt).write_file(promot))
        
        if manual:
            session_id = input("session_id")
        else:
            o = self.client.new(self.repo_root.path).start_server()
            result = o.do_prompt(promot)
            session_id = result.data["session_id"]
            final_result = o.wait_result(session_id, timeout=1800)
            o.stop()
            if not final_result.ok:
                logger.error(f"LLM 任务失败: {final_result.title}")
                self.src_root.child(Fp.opencode_json).set("session_id", session_id)
                return final_result
        
        diff_content = git.git_diff()
        if diff_content and diff_content.strip():
            self.src_final_diff.write_file(diff_content)
            logger.info(f"生成 final.diff: {self.src_final_diff.path}")
        else:
            logger.warning("git diff 为空，LLM 未修改代码")
        
        self.src_root.child(Fp.opencode_json).set("session_id", value=session_id)
        logger.info(f"LLM 完成, session_id={session_id}")
   
    def docker_build(self):
        image_name = self.env
        self._docker_build(self.tmp_root, image_name)
        logger.info(f"Docker build completed: {image_name}")
        return image_name

    def _copy_task_files(self, files_to_copy):
        for f in files_to_copy:
            src_file = self.src_root.child(f)
            dst_file = self.tmp_root.child(f)
            dst_file.write_file(src_file.read_file())

    def _patch_network_config(self, tmp_root: File):
        from common.tool.export import GC

        def _str(val):
            return str(val) if val else ""

        dockerfile = tmp_root.child("Dockerfile")
        if dockerfile.exists():
            content = dockerfile.read_file()

            if GC.zb_docker_env:
                zb_env = _str(GC.zb_docker_env)
                content = re.sub(
                    r'^FROM\s+(\S+)',
                    lambda m: f"FROM {zb_env}/library/{m.group(1)}"
                    if "/" not in m.group(1)
                    else f"FROM {zb_env}/{m.group(1)}",
                    content,
                    flags=re.MULTILINE,
                )

            if GC.apt_mirror_prefix:
                apt_mirror = _str(GC.apt_mirror_prefix)
                content = re.sub(
                    r"sed -i 's@archive\.ubuntu\.com@(\S+)@g'",
                    f"sed -i 's@archive.ubuntu.com@{apt_mirror}@g'",
                    content,
                )
                content = re.sub(
                    r"sed -i 's@security\.ubuntu\.com@(\S+)@g'",
                    f"sed -i 's@security.ubuntu.com@{apt_mirror}@g'",
                    content,
                )

            if GC.pip_global_index_url:
                pip_url = _str(GC.pip_global_index_url)
                content = re.sub(
                    r'pip config set global\.index-url\s+\S+',
                    f'pip config set global.index-url {pip_url}',
                    content,
                )
            if GC.pip_trusted_host:
                pip_host = _str(GC.pip_trusted_host)
                content = re.sub(
                    r'pip config set global\.trusted-host\s+\S+',
                    f'pip config set global.trusted-host {pip_host}',
                    content,
                )

            if GC.miniconda_mirror:
                miniconda = _str(GC.miniconda_mirror)
                content = re.sub(
                    r"https://repo\.anaconda\.com/miniconda/",
                    miniconda,
                    content,
                )

            if GC.conda_channel_prefix:
                conda_channel = _str(GC.conda_channel_prefix)
                content = re.sub(
                    r"conda config --add channels\s+(\S+)",
                    f"conda config --add channels {conda_channel}",
                    content,
                )

            dockerfile.write_file(content)

        for script_name in ["setup_env.sh", "setup_repo.sh"]:
            script = tmp_root.child(script_name)
            if not script.exists():
                continue

            content = script.read_file()

            if GC.http_proxy:
                http_proxy = _str(GC.http_proxy)
                proxy_block = f"export HTTP_PROXY={http_proxy}\nexport HTTPS_PROXY={http_proxy}\nexport GIT_SSL_NO_VERIFY=1\n"
                if not re.search(r'export HTTP_PROXY', content):
                    content = re.sub(
                        r'^(#!.*\n)',
                        f'$1\n{proxy_block}',
                        content,
                    )

            if GC.git_proxy_prefix:
                git_proxy = _str(GC.git_proxy_prefix)
                content = re.sub(
                    r"git clone https://github\.com/",
                    f"git clone https://{git_proxy}/github.com/",
                    content,
                )

            if GC.pip_global_index_url:
                pip_url = _str(GC.pip_global_index_url)
                content = re.sub(
                    r'-i\s+https://[^\s]+',
                    f'-i {pip_url}',
                    content,
                )

            content = re.sub(
                r"conda create\s+",
                "CONDA_SOLVER=classic conda create ",
                content,
            )

            if GC.miniconda_mirror:
                miniconda = _str(GC.miniconda_mirror)
                content = content.replace(
                    "https://repo.anaconda.com/miniconda/",
                    miniconda,
                )

            script.write_file(content)

    def _docker_build(self, tmp_root: File, image_name: str):
        logger.info(f"Running: docker build -t {image_name}")
        self._copy_task_files(Fp.docker_build())
        self._patch_network_config(tmp_root)
        DockerUtil().build(image_name, tmp_root.get_abs_path())
        logger.info(f"Docker build success: {image_name}")

    def check(self):
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
        self._copy_task_files(Fp.pre_check())
        self.check()

    def llm_check(self):
        self._copy_task_files(Fp.llm_check())
        code_patch = self.tmp_root.child(Fp.code_patch)
        self.tmp_root.child(Fp.final_diff).move_to(code_patch)
        self.check()
