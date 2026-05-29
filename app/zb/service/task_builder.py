import subprocess
import shutil
import os

from common.third_util.llm.opencode_client import OpencodeClient, logger
from common.util.export import File

from ..model.constants import Fp, ROOT, PROMOT_TEMPLATE


class TaskBuilder:
    def __init__(self, opencode_client=None):
        self.client = opencode_client or OpencodeClient

    def build(self, task_root: File, prompt: str = None):
        prompt = prompt or PROMOT_TEMPLATE
        task_root.child(Fp.final_diff).remove()
        o = self.client.new(task_root.path, "http://127.0.0.1:45799").start_server()
        result = o.do_prompt(prompt)
        opencode_json = task_root.child("opencode.json")
        logger.info(opencode_json.write_file(result.to_json()))
        return result

    def build_docker(self, name: str, proxy_host: str = None):
        src_root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        tmp_root = File(f"data/tmp/docker_build/{name}")
        
        tmp_root.remove()
        os.makedirs(tmp_root.path, exist_ok=True)
        
        self._copy_task_files(src_root, tmp_root)
        
        dockerfile = tmp_root.child(Fp.Dockerfile)
        content = dockerfile.read_file(encoding="utf-8")
        
        if "mirrors.tools.huawei.com/pypi/simple" in content:
            logger.info("Dockerfile already has Huawei PyPI mirror, skipping proxy patch")
        else:
            self._patch_dockerfile(dockerfile, proxy_host)
        
        self._patch_setup_env(tmp_root.child(Fp.setup_env_sh), proxy_host)
        
        image_name = name.split("/")[-1].replace("__", "-")
        self._docker_build(tmp_root, image_name)
        
        tmp_root.remove()
        logger.info(f"Docker build completed: {image_name}")
        return image_name

    def _copy_task_files(self, src: File, dst: File):
        files_to_copy = [
            Fp.Dockerfile,
            Fp.setup_env_sh,
            Fp.setup_repo_sh,
            Fp.entrypoint_sh,
            Fp.run_verification_py,
            f"{src.name}.json",
        ]
        for f in files_to_copy:
            src_file = src.child(f)
            if src_file.exists():
                shutil.copy(src_file.path, dst.child(f).path)

    def _patch_dockerfile(self, dockerfile: File, proxy_host: str = None):
        if proxy_host is None:
            proxy_host = "http://proxy.huawei.com:8080"
        
        content = dockerfile.read_file(encoding="utf-8")
        
        proxy_config = f'''
# 配置公司代理
ARG PROXY_HOST={proxy_host}
ENV HTTP_PROXY=${{PROXY_HOST}}
ENV HTTPS_PROXY=${{PROXY_HOST}}
ENV NO_PROXY=localhost,127.0.0.1,mirrors.tools.huawei.com,.huawei.com

# 配置 Ubuntu 华为内部镜像源
RUN sed -i 's@archive.ubuntu.com@mirrors.tools.huawei.com@g' /etc/apt/sources.list && \
    sed -i 's@security.ubuntu.com@mirrors.tools.huawei.com@g' /etc/apt/sources.list

# wget 代理配置
RUN echo "http_proxy = {proxy_host}" >> ~/.wgetrc && \
    echo "https_proxy = {proxy_host}" >> ~/.wgetrc

# pip 代理配置（创建 pip.conf）
RUN mkdir -p ~/.config/pip && \
    echo "[global]" > ~/.config/pip/pip.conf && \
    echo "proxy = {proxy_host}" >> ~/.config/pip/pip.conf && \
    echo "timeout = 120" >> ~/.config/pip/pip.conf

'''
        
        lines = content.split('\n')
        new_lines = []
        inserted = False
        
        for line in lines:
            new_lines.append(line)
            if line.startswith('FROM ') and not inserted:
                new_lines.append(proxy_config)
                inserted = True
        
        dockerfile.write_file('\n'.join(new_lines), encoding="utf-8")

    def _patch_setup_env(self, setup_env: File, proxy_host: str = None):
        if proxy_host is None:
            proxy_host = "http://proxy.huawei.com:8080"
        
        if not setup_env.exists():
            return
        
        content = setup_env.read_file(encoding="utf-8")
        
        lines = content.split('\n')
        new_lines = []
        in_header = True
        
        for line in lines:
            if in_header and line.strip() and not line.startswith('#'):
                new_lines.append(f'export HTTP_PROXY="{proxy_host}"')
                new_lines.append(f'export HTTPS_PROXY="{proxy_host}"')
                new_lines.append(f'export http_proxy="{proxy_host}"')
                new_lines.append(f'export https_proxy="{proxy_host}"')
                new_lines.append(f'export GIT_SSL_NO_VERIFY=1')
                in_header = False
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        if "pip install" in content and "--proxy" not in content:
            content = content.replace(
                "pip install",
                f"pip install --proxy {proxy_host} --timeout 120"
            )
        
        setup_env.write_file(content, encoding="utf-8")

    def _docker_build(self, tmp_root: File, image_name: str):
        logger.info(f"Running: docker build -t {image_name}")
        
        wsl_path = tmp_root.path.replace("D:\\", "/mnt/d/").replace("\\", "/")
        cmd = f"docker build -t {image_name} {wsl_path}"
        
        result = subprocess.run(
            ["wsl", "-e", "bash", "-c", cmd],
            capture_output=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode != 0:
            logger.error(f"Docker build failed: {result.stderr}")
            raise Exception(f"Docker build failed: {image_name}")
        
        logger.info(f"Docker build success: {image_name}")