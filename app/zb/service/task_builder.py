import re
from common.third_util.llm.opencode_client import OpencodeClient, logger
from common.third_util.llm.opencode_db import OpencodeDb
from common.util.export import File
from common.third_service.docker.docker_util import DockerUtil
from common.third_service.git_tool.git_util import GitUtil

from ..model.constants import Fp, OPENCODE_JSON_FILE_NAME,PROMOT_TXT,ROOT, get_promot, fetch_github_issue, REPO_ROOT


class TaskBuilder:
    def __init__(self, opencode_client=None):
        self.client = opencode_client or OpencodeClient

    def set_env(self, name: str):
        self.src_run_verification_py = ROOT.search_one(f"{name}/{Fp.run_verification_py}")
        self.src_root = self.src_run_verification_py.parent()
        self.name = self.src_root.name
        self.env = self.name.split("-")[0]
        
        # 修改 run_verification.py，将 code.patch 替换为 final.diff
        content = self.src_run_verification_py.read_file()
        content = content.replace('"code.patch"', '"final.diff"')
        self.src_run_verification_py.write_file(content)
        
        self.src_test_pattch = self.src_root.child(Fp.test_patch)
        self.tmp_root = (
            File(f"data/tmp/docker_build/{self.name}")
            .remove()
            .make_dir_if_not_exist(is_dir=True)
        )
        self.src_final_diff = self.src_root.child(Fp.final_diff)
        self.instance_json = self.src_root.child(f"{self.src_root.name}.json")
        self.repo_root = REPO_ROOT.child(self.env)

        # entrypoint.sh 非交付件，删除以免 M1 质检报多余文件
        entrypoint = self.src_root.child("entrypoint.sh")
        if entrypoint.exists():
            entrypoint.remove()

        # 清理 Dockerfile 中对 entrypoint.sh 的引用
        dockerfile = self.src_root.child(Fp.Dockerfile)
        content = dockerfile.read_file()
        if content and "entrypoint.sh" in content:
            content = "\n".join(line for line in content.splitlines() if "entrypoint.sh" not in line)
            dockerfile.write_file(content)

        return self

    @property
    def base_commit(self):
        return self.instance_json.get("base_commit")

    @property
    def issue_url(self):
        return self.instance_json.get("issue_url")

    def _ensure_repo(self):
        if self.repo_root.exists():
            return
        repo_path = self.instance_json.get("repo")
        clone_url = f"https://github.com/{repo_path}.git"
        parent = self.repo_root.parent()
        parent.make_dir_if_not_exist(is_dir=True)
        GitUtil(workdir=parent.path).git_clone(clone_url, self.repo_root.name)

    def _save_initial_state(self, git, diff_content):
        files = re.findall(r"^diff --git a/(.*?) b/", diff_content, re.MULTILINE)
        initial_state = {}
        for f in files:
            content = git.git_show(f"{self.base_commit}:{f}")
            if content:
                initial_state[f] = content
        opencode_json = self.src_root.child(OPENCODE_JSON_FILE_NAME)
        data = opencode_json.read_file() if opencode_json.exists() else {}
        data["initial_state"] = initial_state
        opencode_json.write_file(data)
        logger.info(f"保存 initial_state: {list(initial_state.keys())}")

    def llm_build(self, manual=False):
        self._ensure_repo()
        git = GitUtil(workdir=self.repo_root.path)
        git.git_clean()
        git.git_reset(self.base_commit)
        git.git_apply(self.src_test_pattch.path)
        git.git_add(".")
        logger.info(f"Git reset to {self.base_commit}, applied test.patch {self.repo_root}")

        opencode_json = self.src_root.child(OPENCODE_JSON_FILE_NAME)
        opencode_data = opencode_json.read_file() if opencode_json.exists() else {}
        existing_session_id = opencode_data.get("session_id")
        db = OpencodeDb.get_instance()

        if existing_session_id and db.is_session_complete(existing_session_id):
            logger.info(f"[跳过 LLM] session {existing_session_id} 已完成")
            return existing_session_id

        issue_content = self.instance_json.get("problem_statement")

        test_patch_content = self.src_test_pattch.read_file() if self.src_test_pattch.exists() else None

        promot_mock_file = self.src_root.child("promot_mock.txt")
        mock_content = promot_mock_file.read_file() if promot_mock_file.exists() else None

        promot = get_promot(
            self.issue_url,
            issue_content=issue_content,
            fail_to_pass=self.instance_json.get("FAIL_TO_PASS"),
            pass_to_pass=self.instance_json.get("PASS_TO_PASS"),
            test_patch_content=test_patch_content,
            mock_prompt=mock_content,
        )
        logger.info(self.src_root.child(PROMOT_TXT).write_file(promot))

        if manual:
            session_id = input("session_id")
        else:
            o = self.client.new(self.repo_root.path).start_server()

            if existing_session_id and db.has_data(existing_session_id):
                session_id = existing_session_id
                logger.info(f"[继续] session {session_id} 进行中")
            else:
                s = o.create_session()
                session_id = s.id
                opencode_json.write_file({"session_id": session_id})
                o.execute_task(session_id, promot)
                logger.info(f"[新建] session {session_id}")

            final_result = o.wait_result(session_id, timeout=1800, stall_timeout=900)
            o.stop()
            if not final_result.ok:
                logger.error(f"LLM 任务失败: {final_result.title}")

        opencode_json.write_file({"session_id": session_id})
        diff_content = git.git_diff()
        if diff_content and diff_content.strip():
            self.src_final_diff.write_file(diff_content)
            logger.info(f"生成 final.diff: {self.src_final_diff.path}")
            self._save_initial_state(git, diff_content)
        else:
            logger.warning("git diff 为空，LLM 未修改代码")
        git.git_reset(self.base_commit)
        git.git_clean()
        logger.info(f"LLM 完成, session_id={session_id}")
   
    def docker_build(self):
        image_name = f"{self.env}:{self.name.split('-')[-1]}"
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

            if GC.zb_docker_env.get_value():
                zb_env = _str(GC.zb_docker_env)
                content = re.sub(
                    r'^FROM\s+(\S+)',
                    lambda m: f"FROM {zb_env}/library/{m.group(1)}"
                    if "/" not in m.group(1)
                    else f"FROM {zb_env}/{m.group(1)}",
                    content,
                    flags=re.MULTILINE,
                )

            if GC.apt_mirror_prefix.get_value():
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

            if GC.pip_global_index_url.get_value():
                pip_url = _str(GC.pip_global_index_url)
                content = re.sub(
                    r'pip config set global\.index-url\s+\S+',
                    f'pip config set global.index-url {pip_url}',
                    content,
                )
            if GC.pip_trusted_host.get_value():
                pip_host = _str(GC.pip_trusted_host)
                content = re.sub(
                    r'pip config set global\.trusted-host\s+\S+',
                    f'pip config set global.trusted-host {pip_host}',
                    content,
                )

            if GC.miniconda_mirror.get_value():
                miniconda = _str(GC.miniconda_mirror)
                content = re.sub(
                    r"https://repo\.anaconda\.com/miniconda/",
                    miniconda,
                    content,
                )

            if GC.conda_channel_prefix.get_value():
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

            if GC.http_proxy.get_value():
                http_proxy = _str(GC.http_proxy)
                proxy_block = f"export HTTP_PROXY={http_proxy}\nexport HTTPS_PROXY={http_proxy}\nexport GIT_SSL_NO_VERIFY=1\n"
                if not re.search(r'export HTTP_PROXY', content):
                    content = re.sub(
                        r'^(#!.*\n)',
                        f'$1\n{proxy_block}',
                        content,
                    )

            content = re.sub(
                r"git clone https://[^/]+/github\.com/",
                "git clone https://github.com/",
                content,
            )

            if GC.pip_global_index_url.get_value():
                pip_url = _str(GC.pip_global_index_url)
                pip_config = f"pip config set global.index-url {pip_url}\n"
                if GC.pip_trusted_host.get_value():
                    pip_host = _str(GC.pip_trusted_host)
                    pip_config += f"pip config set global.trusted-host {pip_host}\n"
                content = re.sub(
                    r'^(#!.*\n)?',
                    lambda m: (m.group(1) or "") + pip_config,
                    content,
                    count=1,
                )
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
            content = re.sub(
                r"^CONDA_SOLVER=classic conda create .+$",
                lambda m: f"for _ in 1 2 3; do {m.group(0)} && break; sleep 10; done",
                content,
                flags=re.MULTILINE,
            )

            if GC.miniconda_mirror.get_value():
                miniconda = _str(GC.miniconda_mirror)
                content = content.replace(
                    "https://repo.anaconda.com/miniconda/",
                    miniconda,
                )

            if GC.conda_mirror.get_value() and script_name == "setup_env.sh":
                conda_mirror = _str(GC.conda_mirror)
                content = content.replace(
                    "CONDA_SOLVER=classic conda create ",
                    f"conda config --add channels {conda_mirror}/pkgs/main/ 2>/dev/null || true\n"
                    f"conda config --add channels {conda_mirror}/pkgs/r/ 2>/dev/null || true\n"
                    f"conda config --set show_channel_urls yes 2>/dev/null || true\n\n"
                    f"CONDA_SOLVER=classic conda create ",
                )

            content = re.sub(
                r"(?<!uv )pip install(?!\s+--default-timeout)",
                "pip install --default-timeout=120",
                content,
            )

            script.write_file(content)

    def _docker_build(self, tmp_root: File, image_name: str):
        logger.info(f"Running: docker build -t {image_name}")
        self._copy_task_files(Fp.docker_build())
        self._patch_network_config(tmp_root)
        DockerUtil().build(image_name, tmp_root.get_abs_path())
        logger.info(f"Docker build success: {image_name}")

    def check(self):
        image_name = f"{self.env}:{self.name.split('-')[-1]}"
        abs_path = self.tmp_root.get_abs_path()
        try:
            DockerUtil().run_container(
                image=image_name,
                detach=False,
                rm=True,
                network="none",
                volumes={abs_path: "/testbed/verification"},
                cmd="export PATH=/opt/miniconda3/envs/testbed/bin:$PATH && python /testbed/verification/run_verification.py",
            )
        except Exception:
            pass

        results_json = self.tmp_root.child("results.json")
        if results_json.exists():
            return results_json.read_file()
        return None

    def pre_check(self):
        self._copy_task_files(Fp.pre_check())
        code_patch = self.tmp_root.child(Fp.code_patch)
        if code_patch.exists():
            code_patch.move_to(self.tmp_root.child(Fp.final_diff))
        result = self.check()
        self._assert_check_passed(result, "pre_check")

    def llm_check(self):
        self._copy_task_files(Fp.llm_check())
        result = self.check()
        self._assert_check_passed(result, "llm_check")

    def _assert_check_passed(self, result, step_name):
        if result is None:
            raise Exception(f"{step_name} 失败: results.json 未生成")
        if isinstance(result, dict):
            inner = result.get(self.name, result)
            if isinstance(inner, dict) and not inner.get("resolved", True):
                fail_fail = inner.get("tests_status", {}).get("FAIL_TO_FAIL", {})
                fail_count = len(fail_fail.get("failure", []))
                raise Exception(f"{step_name} 失败: {fail_count} 个测试未修复")
        logger.info(f"{step_name} 通过")
