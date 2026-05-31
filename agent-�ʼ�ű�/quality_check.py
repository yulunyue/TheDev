#!/usr/bin/env python3
"""
User-Agentic 数据集质检脚本
"""

import argparse
import json
import logging
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from datetime import datetime


# ========== 日志配置 ==========

def setup_logger(log_file: str | None = None, verbose: bool = True) -> logging.Logger:
    """配置日志记录器。
    
    Args:
        log_file: 日志文件路径，如果为 None 则只输出到控制台
        verbose: 是否输出详细日志到控制台
    
    Returns:
        配置好的 logger 实例
    """
    logger = logging.getLogger("quality_check")
    logger.setLevel(logging.DEBUG)
    
    # 清除已有的 handlers
    logger.handlers.clear()
    
    # 创建 formatter
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件 handler - 始终记录详细日志
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    # 控制台 handler - 根据 verbose 参数决定是否输出
    if verbose:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger


# 全局 logger 实例
logger = setup_logger()

# ========== 模块开关 — 设为 False 可跳过对应检查 ==========

ENABLE_M1_FILE_COMPLETENESS = True      # 交付文件完备性
ENABLE_M2_INSTANCE_JSON = True          # instance.json 字段验证
ENABLE_M3_TRAJECTORY_JSON = True       # trajectory.json 格式与字段
ENABLE_M4_PATCH_SIMILARITY = False       # code.patch vs final.diff 相似度（已禁用）
ENABLE_M5_PROMPT_LEAKAGE = False         # 提示词泄漏检测（已禁用）
ENABLE_M6_INITIAL_STATE = True          # 初始状态验证（需 Docker）
ENABLE_M7_VERIFICATION = True           # 回归验证（需 Docker）
ENABLE_M8_NO_DATA_VERIFICATION = True    # 不依赖脚本的回归验证（需 Docker）
ENABLE_M9_TRAJECTORY_FIELD_NAMES = True   # trajectory.json 字段名完备性（对比 example）
ENABLE_M10_SYSTEM_PROMPT = True           # coding_agent_system_prompt 相似度校验
ENABLE_M11_CUSTOM_CHECK = True           # 自定义一致性与重合度校验

# trajectory.json 读取格式控制
# True: 按 JSON 格式读取 (每行一个 JSON 对象)
# False: 按标准 JSON 格式读取 (整个文件是一个 JSON 对象或数组)
ENABLE_JSON_FORMAT = False

SAVE_JSON_REPORT = False  # 是否保存 JSON 报告文件

# 交付文件列表

REQUIRED_DELIVERY_FILES = [
    "code.patch",
    "test.patch",
    "final.diff",
    "trajectory.json",
    "Dockerfile",
    "setup_env.sh",
    "setup_repo.sh",
    "run_verification.py",
]


# instance.json 必填字段 {字段名: 期望类型}
INSTANCE_REQUIRED_FIELDS = {
    "instance_id": str,
    "repo": str,
    "base_commit": str,
    "language": (str, list),
    "problem_statement": str,
    "FAIL_TO_PASS": (str, list),
    "PASS_TO_PASS": (str, list),
    "patch": str,
    "test_patch": str,
}

# trajectory.json 字段定义

TRAJECTORY_TOP_FIELDS = {
    "instance_id": str,
    "instruction": str,
    "instance": dict,
    "metadata": dict,
    "trajectory": list,
    "task_category": str,
}

TRAJECTORY_INSTANCE_FIELDS = {
    "repo": str,
    "base_commit": str,
    "git_context": dict,
    "problem_statement": str,
    "FAIL_TO_PASS": (str, list),
    "PASS_TO_PASS": (str, list),
    "patch": str,
    "test_patch": str,
}

TRAJECTORY_GIT_CONTEXT_FIELDS = {
    "initial_state": (dict, str),
    "final_diff": str,
}

TRAJECTORY_METADATA_FIELDS = {
    "agent": str,
    "model": str,
    "thinking_mode": str,
    "eval_output_dir": str,
    "data_source": str,
    "source": str,
    # "model_system_prompt": (str, list),
    "coding_agent_system_prompt": str,
    "tools": list,
}

# task_category 合法枚举值
VALID_TASK_CATEGORIES = {"bug_fix", "feature"}





# Example 目录路径（用于 M9 字段名完备性和 M10 系统提示词相似度对比）
EXAMPLE_DIR = Path(__file__).parent / "example"

# M10: 系统提示词相似度阈值
SYSTEM_PROMPT_SIMILARITY_LOWER_BOUND = 0.95   # 相似度 > 此值
SYSTEM_PROMPT_SIMILARITY_UPPER_BOUND = 1.0    # 且不等于此值


#  回归验证配置
VERIFICATION_TIMEOUT = 600              # 验证超时秒数
VERIFICATION_SCRIPT_NAMES = [           # 按优先级查找的脚本文件名
    "run_verification.py",
    "verification.py",
]
VERIFICATION_MOUNT_FILES = [            # 需要挂载进容器的文件
    # "code.patch",
    "test.patch",
    "final.diff",
]


# 通用配置
REPORT_EXCLUDES = {"qc_report.json", "results.json", "result.json"}

LANGUAGE = []
ERROR_MESSAGES = []
CONDA_ENV_CACHE: dict[str, tuple[bool, str | None]] = {}


def reset_runtime_state() -> None:
    """重置单次质检运行态，避免多任务之间互相污染。"""
    global LANGUAGE, ERROR_MESSAGES
    LANGUAGE = []
    ERROR_MESSAGES = []


@dataclass
class Issue:
    """单条检查结果。"""
    code: str
    message: str
    severity: str  # error / warning / info

    def to_dict(self) -> dict:
        return {"code": self.code, "message": self.message, "severity": self.severity}


@dataclass
class ModuleReport:
    """单模块检查报告。"""
    name: str
    passed: bool = True
    issues: list[Issue] = field(default_factory=list)

    def add(self, code: str, message: str, severity: str = "error") -> None:
        self.issues.append(Issue(code, message, severity))
        if severity == "error":
            self.passed = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "passed": self.passed,
            "error_count": sum(1 for i in self.issues if i.severity == "error"),
            "warning_count": sum(1 for i in self.issues if i.severity == "warning"),
            "issues": [i.to_dict() for i in self.issues],
        }


def _skipped_report(name: str, reason: str) -> ModuleReport:
    """生成一个被开关关闭的模块报告。"""
    report = ModuleReport(name=name)
    report.add(f"{name.split('-')[0]}-OFF", reason, "info")
    logger.info(f"[{name}] 模块已跳过：{reason}")
    return report



def load_text(path: Path) -> str:
    """读取文本文件内容。"""
    if not path.is_file():
        logger.debug(f"[文件读取] 文件不存在：{path}")
        return ""
    logger.debug(f"[文件读取] 读取文件：{path}")
    content = path.read_text(encoding="utf-8", errors="replace")
    logger.debug(f"[文件读取] 文件大小：{len(content)} 字符")
    return content


def load_json(path: Path) -> dict | None:
    """加载 JSON 文件。"""
    logger.debug(f"[JSON 加载] 尝试加载：{path}")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            logger.debug(f"[JSON 加载] 成功加载：{path}, keys={list(data.keys()) if isinstance(data, dict) else 'list'}")
            return data
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"[JSON 加载] 失败：{path}, 错误：{e}")
        global ERROR_MESSAGES
        ERROR_MESSAGES.append(f"[JSON 加载] 错误：{path}, 错误：{e}")
        return None


def load_trajectory_json(path: Path, force_json_format: bool = False) -> tuple[list[dict], list[str]]:
    """加载 JSON 文件。
    
    Args:
        path: 文件路径
        force_json_format: 是否强制按 JSON 格式读取
            - True: 将整个文件作为单个 JSON 对象或数组解析
            - False: 按 JSON 格式逐行解析 (默认)
    
    Returns:
        (records, errors): 记录列表和解析错误列表
    """
    logger.debug(f"[JSON 加载] 尝试加载：{path}, 强制 JSON 模式={force_json_format}")
    content = load_text(path)
    if not content.strip():
        logger.warning(f"[JSON 加载] 文件为空：{path}")
        return [], ["文件为空"]

    records: list[dict] = []
    errors: list[str] = []

    # 如果强制使用 JSON 格式，直接解析整个文件
    if force_json_format:
        try:
            obj = json.loads(content)
            if isinstance(obj, dict):
                logger.debug(f"[JSON 加载] JSON 模式：检测到单条 JSON 对象")
                return [obj], []
            elif isinstance(obj, list):
                valid_records = [o for o in obj if isinstance(o, dict)]
                logger.debug(f"[JSON 加载] JSON 模式：检测到 JSON 数组，共 {len(valid_records)} 条记录")
                return valid_records, []
            else:
                logger.error(f"[JSON 加载] JSON 模式：根元素不是对象或数组")
                global ERROR_MESSAGES
                ERROR_MESSAGES.append(f"[JSON 加载] JSON 模式：根元素不是对象或数组")
                return [], ["JSON 根元素不是对象或数组"]
        except json.JSONDecodeError as exc:
            logger.error(f"[JSON 加载] JSON 模式解析失败：{exc}")
            ERROR_MESSAGES.append(f"[JSON 加载] JSON 模式解析失败：{exc}")
            return [], [f"JSON 解析失败：{exc}"]

    # 默认 JSON 格式：逐行解析
    try:
        # 先尝试作为单个 JSON 对象解析 (兼容格式化输出)
        obj = json.loads(content)
        if isinstance(obj, dict):
            logger.debug(f"[JSON 加载] 检测到单条 JSON 对象")
            return [obj], []
        if isinstance(obj, list):
            logger.debug(f"[JSON 加载] 检测到 JSON 数组，共 {len(obj)} 条记录")
            return [o for o in obj if isinstance(o, dict)], []
    except json.JSONDecodeError:
        pass

    # 逐行解析 JSON
    for idx, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
            if isinstance(record, dict):
                records.append(record)
        except json.JSONDecodeError as exc:
            error_msg = f"第 {idx} 行 JSON 解析失败：{exc}"
            ERROR_MESSAGES.append(error_msg)
            errors.append(error_msg)
            logger.error(f"[JSON 加载] {error_msg}")

    logger.debug(f"[JSON 加载] 成功加载 {len(records)} 条记录，{len(errors)} 个错误")
    return records, errors


def find_instance_json(project_dir: Path) -> Path | None:
    """查找 instance.json 文件。"""
    logger.debug(f"[实例 JSON 查找] 在目录中搜索：{project_dir}")
    
    # 规则 1: 清洗可能存在的临时解压目录前缀，尝试精确匹配
    cleaned_dir_name = project_dir.name
    if cleaned_dir_name.startswith(".temp_extracted_"):
        cleaned_dir_name = cleaned_dir_name.replace(".temp_extracted_", "")
        
    candidates = [
        f for f in project_dir.glob(f"{cleaned_dir_name}.json")
        if f.name not in REPORT_EXCLUDES
    ]
    
    # 规则 2: 如果目录名不匹配，退避搜索所有含双下划线 "__" 的 json 文件（排除 report 与 trajectory）
    if not candidates:
        candidates = [
            f for f in project_dir.glob("*.json")
            if f.name not in REPORT_EXCLUDES and f.name != "trajectory.json" and "__" in f.name
        ]
        
    # 规则 3: 进一步退避搜寻所有 json 文件（排除 report 与 trajectory）
    if not candidates:
        candidates = [
            f for f in project_dir.glob("*.json")
            if f.name not in REPORT_EXCLUDES and f.name != "trajectory.json"
        ]
        
    logger.debug(f"[实例 JSON 查找] 找到 {len(candidates)} 个候选文件：{[f.name for f in candidates]}")
    
    if not candidates:
        global ERROR_MESSAGES
        if "[实例 JSON 查找] 未找到任何 JSON 文件" not in ERROR_MESSAGES:
            ERROR_MESSAGES.append("[实例 JSON 查找] 未找到任何 JSON 文件")
        logger.warning("[实例 JSON 查找] 未找到任何 JSON 文件")
        return None
        
    for f in candidates:
        if "__" in f.stem:
            logger.info(f"[实例 JSON 查找] 选择文件：{f.name} (包含 __ 分隔符)")
            return f
            
    selected = candidates[0]
    logger.info(f"[实例 JSON 查找] 选择第一个文件：{selected.name}")
    return selected





def docker_exec(container_id: str, command: str, timeout: int = 30) -> tuple[bool, str]:
    """在 Docker 容器中执行命令。"""
    global ERROR_MESSAGES
    logger.debug(f"[Docker 执行] 容器 ID: {container_id[:12]}")
    logger.debug(f"[Docker 执行] 命令：{command}")
    
    try:
        result = subprocess.run(
            ["docker", "exec", container_id, "bash", "-c", command],
            capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace"
        )
        
        success = result.returncode == 0
        logger.debug(f"[Docker 执行] 返回码：{result.returncode}, 成功：{success}")
        logger.debug(f"[Docker 执行] 输出长度：{len(result.stdout)} 字符")
        
        if result.stdout.strip():
            logger.debug(f"[Docker 执行] STDOUT:\n{result.stdout[:500]}{'... (truncated)' if len(result.stdout) > 500 else ''}")
        if result.stderr.strip():
            logger.warning(f"[Docker 执行] STDERR:\n{result.stderr[:500]}{'... (truncated)' if len(result.stderr) > 500 else ''}")
        
        return success, result.stdout
    
    except subprocess.TimeoutExpired as exc:
        ERROR_MESSAGES.append(f"[Docker 执行] 超时 ({timeout}s): {command}")
        logger.error(f"[Docker 执行] 超时 ({timeout}s): {command}")
        return False, f"Timeout after {timeout}s"
    except FileNotFoundError as exc:
        ERROR_MESSAGES.append(f"[Docker 执行] Docker 未找到：{exc}")
        logger.error(f"[Docker 执行] Docker 未找到：{exc}")
        return False, str(exc)


def _resolve_shell_value(value: str, variables: dict[str, str]) -> str | None:
    """解析 setup_env.sh 中的简单变量引用。"""
    value = value.strip().strip("\"'")
    match = re.fullmatch(r"\$(?:{(?P<braced>[A-Za-z_][A-Za-z0-9_]*)}|(?P<plain>[A-Za-z_][A-Za-z0-9_]*))", value)
    if not match:
        return value or None
    var_name = match.group("braced") or match.group("plain")
    return variables.get(var_name)


def detect_conda_env(project_dir: Path) -> tuple[bool, str | None]:
    """从 setup_env.sh 中判断是否使用 conda，并尽量提取环境名。"""
    cache_key = str(project_dir.resolve())
    if cache_key in CONDA_ENV_CACHE:
        return CONDA_ENV_CACHE[cache_key]

    setup_env_path = project_dir / "setup_env.sh"
    if not setup_env_path.is_file():
        CONDA_ENV_CACHE[cache_key] = (False, None)
        return CONDA_ENV_CACHE[cache_key]

    content = load_text(setup_env_path)
    if not content:
        CONDA_ENV_CACHE[cache_key] = (False, None)
        return CONDA_ENV_CACHE[cache_key]

    uses_conda = bool(re.search(r"\b(?:conda|mamba|micromamba)\b", content))
    if not uses_conda:
        CONDA_ENV_CACHE[cache_key] = (False, None)
        return CONDA_ENV_CACHE[cache_key]

    variables: dict[str, str] = {}
    assignment_pattern = re.compile(
        r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(['\"]?)([^'\"]+)\2\s*$"
    )
    env_patterns = [
        re.compile(r"\b(?:conda|mamba|micromamba)\s+(?:create|env\s+create)\b.*?(?:-n|--name)\s+([^\s;]+)"),
        re.compile(r"\b(?:conda|mamba|micromamba|source)\s+activate\s+([^\s;]+)"),
    ]

    for raw_line in content.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue

        assignment = assignment_pattern.match(line)
        if assignment:
            variables[assignment.group(1)] = assignment.group(3).strip()
            continue

        for pattern in env_patterns:
            match = pattern.search(line)
            if not match:
                continue
            env_name = _resolve_shell_value(match.group(1), variables)
            if env_name:
                logger.info(f"[Conda] 检测到 Conda 环境：{env_name}")
                CONDA_ENV_CACHE[cache_key] = (True, env_name)
                return CONDA_ENV_CACHE[cache_key]

    logger.info("[Conda] 检测到 setup_env.sh 使用 Conda，但未解析到明确环境名")
    CONDA_ENV_CACHE[cache_key] = (True, None)
    return CONDA_ENV_CACHE[cache_key]


def wrap_with_optional_conda(project_dir: Path, command: str) -> str:
    """为容器内命令按需补充 conda 初始化与环境激活。"""
    uses_conda, env_name = detect_conda_env(project_dir)
    if not uses_conda:
        return command

    conda_init = (
        "__qc_conda_ready=0; "
        "if command -v conda >/dev/null 2>&1; then "
        "__qc_conda_base=$(conda info --base 2>/dev/null); "
        "if [ -n \"$__qc_conda_base\" ] && [ -f \"$__qc_conda_base/etc/profile.d/conda.sh\" ]; then "
        ". \"$__qc_conda_base/etc/profile.d/conda.sh\"; __qc_conda_ready=1; "
        "fi; "
        "fi; "
        "if [ \"$__qc_conda_ready\" -eq 0 ]; then "
        "for __qc_conda_sh in "
        "\"$HOME/miniconda3/etc/profile.d/conda.sh\" "
        "\"$HOME/anaconda3/etc/profile.d/conda.sh\" "
        "\"/opt/conda/etc/profile.d/conda.sh\" "
        "\"/usr/local/conda/etc/profile.d/conda.sh\" "
        "\"/root/miniconda3/etc/profile.d/conda.sh\"; "
        "do "
        "if [ -f \"$__qc_conda_sh\" ]; then . \"$__qc_conda_sh\"; __qc_conda_ready=1; break; fi; "
        "done; "
        "fi; "
        "if [ \"$__qc_conda_ready\" -eq 0 ]; then "
        "echo '[Conda] 检测到该任务需要 Conda，但容器内未找到 conda 初始化脚本' >&2; exit 1; "
        "fi"
    )

    if env_name:
        activate_conda = f"conda activate {shlex.quote(env_name)}"
    else:
        activate_conda = "echo '[Conda] 未解析到环境名，继续使用当前 Conda 环境'"

    return f"{conda_init} && {activate_conda} && {command}"


def check_field_completeness(
    data: dict,
    field_spec: dict[str, type | tuple],
    prefix: str,
    report: ModuleReport,
) -> None:
    """检查字段完备性。"""
    logger.debug(f"[字段检查] 开始检查 {prefix} 规范，共 {len(field_spec)} 个字段")
    global ERROR_MESSAGES
    for field_name, expected_type in field_spec.items():
        value = data.get(field_name)

        if value is None:
            report.add(f"{prefix}-MISSING", f"缺少必填字段：{field_name}")
            ERROR_MESSAGES.append(f"[字段检查] {prefix}: 缺少字段 '{field_name}'")
            logger.warning(f"[字段检查] {prefix}: 缺少字段 '{field_name}'")
            continue

        if isinstance(expected_type, tuple):
            if not isinstance(value, expected_type):
                type_names = "/".join(t.__name__ for t in expected_type)
                report.add(
                    f"{prefix}-TYPE",
                    f"字段 {field_name} 类型错误：期望 {type_names}, "
                    f"实际 {type(value).__name__}",
                )
                ERROR_MESSAGES.append(f"[字段检查] {prefix}: 字段 '{field_name}' 类型错误：期望 {type_names}, 实际 {type(value).__name__}")
                logger.error(f"[字段检查] {prefix}: 字段 '{field_name}' 类型错误：期望 {type_names}, 实际 {type(value).__name__}")
                continue
        else:
            if not isinstance(value, expected_type):
                report.add(
                    f"{prefix}-TYPE",
                    f"字段 {field_name} 类型错误：期望 {expected_type.__name__}, "
                    f"实际 {type(value).__name__}",
                )
                ERROR_MESSAGES.append(f"[字段检查] {prefix}: 字段 '{field_name}' 类型错误：期望 {expected_type.__name__}, 实际 {type(value).__name__}")
                logger.error(f"[字段检查] {prefix}: 字段 '{field_name}' 类型错误：期望 {expected_type.__name__}, 实际 {type(value).__name__}")
                continue

        if isinstance(value, str) and not value.strip():
            report.add(f"{prefix}-EMPTY", f"必填字段为空字符串：{field_name}")
            ERROR_MESSAGES.append(f"[字段检查] {prefix}: 字段 '{field_name}' 为空字符串")
            logger.warning(f"[字段检查] {prefix}: 字段 '{field_name}' 为空字符串")
        elif isinstance(value, (list, dict)) and len(value) == 0:
            ERROR_MESSAGES.append(f"[字段检查] {prefix}: 字段 '{field_name}' 为空容器")
            report.add(f"{prefix}-EMPTY", f"必填字段为空容器：{field_name}")
            logger.warning(f"[字段检查] {prefix}: 字段 '{field_name}' 为空容器")
    
    logger.debug(f"[字段检查] {prefix} 检查完成")


#  文件完备性
def check_file_completeness(project_dir: Path) -> ModuleReport:
    """检查交付文件完备性。"""
    logger.info(f"[M1] 开始检查文件完备性")
    report = ModuleReport(name="M1-文件完备性")
    global ERROR_MESSAGES
    if not ENABLE_M1_FILE_COMPLETENESS:
        return _skipped_report(report.name, "M1 已关闭")

    logger.debug(f"[M1] 需要检查的文件：{REQUIRED_DELIVERY_FILES}")
    
    for filename in REQUIRED_DELIVERY_FILES:
        filepath = project_dir / filename
        if not filepath.is_file():
            ERROR_MESSAGES.append(f"[M1] 文件缺失：{filename}")
            report.add("M1-MISSING", f"缺少交付文件：{filename}")
            logger.error(f"[M1] 文件缺失：{filename}")
        elif filepath.stat().st_size == 0:
            ERROR_MESSAGES.append(f"[M1] 文件为空：{filename} (大小：0 bytes)")
            report.add("M1-EMPTY", f"交付文件为空：{filename}")
            logger.warning(f"[M1] 文件为空：{filename} (大小：0 bytes)")
        else:
            size_kb = filepath.stat().st_size / 1024
            logger.debug(f"[M1] 文件存在：{filename} (大小：{size_kb:.2f} KB)")

    instance_json = find_instance_json(project_dir)
    if instance_json is None:
        ERROR_MESSAGES.append(f"[M1] 未找到 instance JSON 文件 (*.json)")
        report.add("M1-MISSING", "未找到 instance JSON 文件 (*.json)")
        logger.error(f"[M1] 未找到 instance JSON 文件")
    else:
        logger.info(f"[M1] 找到 instance JSON: {instance_json.name}")

    # 额外多余文件检查
    try:
        all_files = {f.name for f in project_dir.iterdir() if f.is_file()}
        report_excludes = REPORT_EXCLUDES | {instance_json.name if instance_json else ""}
        extra_files = sorted(all_files - set(REQUIRED_DELIVERY_FILES) - report_excludes)
        if extra_files:
            report.add(
                "M1-EXTRA",
                f"存在额外多余文件：{', '.join(extra_files)}",
                "error",
            )
            ERROR_MESSAGES.append(f"[M1] 存在额外多余文件：{', '.join(extra_files)}")
            logger.error(f"[M1] 存在额外多余文件：{', '.join(extra_files)}")
    except Exception as e:
        logger.warning(f"[M1] 额外多余文件检查失败：{e}")

    # Mac 垃圾文件夹 __MACOSX 检查
    if (project_dir / "__MACOSX").is_dir():
        report.add("M1-MACOSX", "发现 __MACOSX 文件夹，请删除", "error")
        ERROR_MESSAGES.append("[M1] 发现 __MACOSX 文件夹，请删除")
        logger.error("[M1] 发现 __MACOSX 文件夹，请删除")

    logger.info(f"[M1] 文件完备性检查完成，错误数：{sum(1 for i in report.issues if i.severity == 'error')}")
    return report



# instance.json 验证
def check_instance_json(project_dir: Path) -> ModuleReport:
    """检查 instance.json 字段。"""
    logger.info(f"[M2] 开始检查 instance.json")
    report = ModuleReport(name="M2-instance.json")
    global ERROR_MESSAGES
    if not ENABLE_M2_INSTANCE_JSON:
        global ENABLE_M8_NO_DATA_VERIFICATION
        ENABLE_M8_NO_DATA_VERIFICATION = False
        return _skipped_report(report.name, "M2 已关闭")

    instance_path = find_instance_json(project_dir)
    if instance_path is None:
        ERROR_MESSAGES.append(f"[M2] 未找到 instance JSON 文件 (*.json)")
        report.add("M2-LOAD", "未找到 instance JSON 文件，跳过检查")
        logger.warning(f"[M2] 未找到 instance JSON 文件，跳过检查")
        return report

    data = load_json(instance_path)
    if data is None:
        ERROR_MESSAGES.append(f"[M2] JSON 解析失败：{instance_path.name}")
        report.add("M2-LOAD", f"JSON 解析失败：{instance_path.name}")
        logger.error(f"[M2] JSON 解析失败：{instance_path.name}")
        return report

    logger.debug(f"[M2] instance.json 包含字段：{list(data.keys())}")
    check_field_completeness(data, INSTANCE_REQUIRED_FIELDS, "M2", report)
    # 获取language字段
    language = data.get("language", [])
    print(f"[M2] language: {language}")
    if type(language) == str:
        global LANGUAGE
        LANGUAGE=[language]
    else:
        LANGUAGE = [lang.strip() for lang in language if lang.strip()]
    # print(f"[M2] LANGUAGE: {LANGUAGE}")
    category = data.get("task_category", "")
    if category and category not in VALID_TASK_CATEGORIES:
        ERROR_MESSAGES.append(f"[M2] task_category 非法：'{category}', 合法值：{VALID_TASK_CATEGORIES}")
        report.add(
            "M2-ENUM",
            f"task_category 非法：'{category}', 合法值：{VALID_TASK_CATEGORIES}",
        )
        logger.error(f"[M2] task_category 非法：'{category}'")
    else:
        logger.debug(f"[M2] task_category: '{category}'")

    logger.info(f"[M2] instance.json 检查完成，错误数：{sum(1 for i in report.issues if i.severity == 'error')}")
    return report

#  trajectory.json 格式与字段验证
def check_trajectory_json(project_dir: Path) -> ModuleReport:
    """检查 trajectory.json 格式与字段。"""
    logger.info(f"[M3] 开始检查 trajectory.json")
    report = ModuleReport(name="M3-trajectory.json")
    global ERROR_MESSAGES
    if not ENABLE_M3_TRAJECTORY_JSON:
        return _skipped_report(report.name, "M3 已关闭")

    json_path = project_dir / "trajectory.json"
    if not json_path.is_file():
        ERROR_MESSAGES.append(f"[M3] trajectory.json 不存在")
        report.add("M3-LOAD", "trajectory.json 不存在")
        logger.error(f"[M3] trajectory.json 不存在")
        return report

    # 根据全局开关决定读取格式
    records, parse_errors = load_trajectory_json(json_path, force_json_format=not ENABLE_JSON_FORMAT)
    for err in parse_errors:
        ERROR_MESSAGES.append(f"[M3] 解析错误：{err}")
        report.add("M3-PARSE", err)
        logger.error(f"[M3] 解析错误：{err}")

    if not records:
        ERROR_MESSAGES.append(f"[M3] trajectory.json 无有效记录")
        report.add("M3-LOAD", "trajectory.json 无有效记录")
        logger.error(f"[M3] trajectory.json 无有效记录")
        return report

    logger.info(f"[M3] 加载了 {len(records)} 条记录 (格式：{'JSON' if not ENABLE_JSON_FORMAT else 'JSON'})")
    
    for idx, record in enumerate(records):
        logger.debug(f"[M3] 检查第 {idx+1} 条记录")
        check_field_completeness(record, TRAJECTORY_TOP_FIELDS, "M3-TOP", report)

        category = record.get("task_category", "")
        if category and category not in VALID_TASK_CATEGORIES:
            report.add(
                "M3-ENUM",
                f"task_category 非法：'{category}', 合法值：{VALID_TASK_CATEGORIES}",
            )
            ERROR_MESSAGES.append(f"[M3] task_category 非法：'{category}', 合法值：{VALID_TASK_CATEGORIES}")
            logger.error(f"[M3] task_category 非法：'{category}'")

        instance = record.get("instance")
        if isinstance(instance, dict):
            logger.debug(f"[M3] 检查 instance 字段")
            check_field_completeness(instance, TRAJECTORY_INSTANCE_FIELDS, "M3-INST", report)

            git_ctx = instance.get("git_context")
            if isinstance(git_ctx, dict):
                logger.debug(f"[M3] 检查 git_context 字段")
                check_field_completeness(
                    git_ctx, TRAJECTORY_GIT_CONTEXT_FIELDS, "M3-GIT", report,
                )
                diff = git_ctx.get("final_diff", "")
                if isinstance(diff, str) and diff.strip() and "diff --git" not in diff:
                    report.add(
                        "M3-DIFF",
                        "final_diff 缺少 Diff Header (diff --git a/... b/...)",
                    )
                    ERROR_MESSAGES.append(f"[M3] final_diff 缺少 Diff Header")
                    logger.warning(f"[M3] final_diff 缺少 Diff Header")
        elif instance is not None:
            ERROR_MESSAGES.append(f"[M3] record[{idx}]: instance 字段不是 dict")
            report.add("M3-TOP-TYPE", f"record[{idx}]: instance 字段不是 dict")
            logger.error(f"[M3] record[{idx}]: instance 字段不是 dict")

        metadata = record.get("metadata")
        if isinstance(metadata, dict):
            logger.debug(f"[M3] 检查 metadata 字段")
            check_field_completeness(metadata, TRAJECTORY_METADATA_FIELDS, "M3-META", report)

        traj = record.get("trajectory")
        if isinstance(traj, list):
            logger.debug(f"[M3] 检查 trajectory 数组 ({len(traj)} 条消息)")
            _check_trajectory_array(traj, report)

    logger.info(f"[M3] trajectory.json 检查完成，错误数：{sum(1 for i in report.issues if i.severity == 'error')}")
    return report


def _check_trajectory_array(traj: list, report: ModuleReport) -> None:
    """检查 trajectory 数组内容。"""
    global ERROR_MESSAGES
    if not traj:
        ERROR_MESSAGES.append(f"[M3-TRAJ] trajectory 数组为空")
        report.add("M3-TRAJ", "trajectory 数组为空")
        logger.warning(f"[M3-TRAJ] trajectory 数组为空")
        return

    roles = []
    tool_use_ids: set[str] = set()
    tool_result_ids: set[str] = set()

    for idx, msg in enumerate(traj):
        if not isinstance(msg, dict):
            ERROR_MESSAGES.append(f"[M3-TRAJ] trajectory[{idx}] 不是 dict")
            report.add("M3-TRAJ", f"trajectory[{idx}] 不是 dict")
            logger.error(f"[M3-TRAJ] trajectory[{idx}] 不是 dict")
            continue

        role = msg.get("role")
        if role is None:
            ERROR_MESSAGES.append(f"[M3-TRAJ] trajectory[{idx}] 缺少 role")
            report.add("M3-TRAJ", f"trajectory[{idx}] 缺少 role")
            logger.warning(f"[M3-TRAJ] trajectory[{idx}] 缺少 role")
        else:
            roles.append(role)

        content = msg.get("content")
        if content is None:
            ERROR_MESSAGES.append(f"[M3-TRAJ] trajectory[{idx}] 缺少 content")
            report.add("M3-TRAJ", f"trajectory[{idx}] 缺少 content")
            logger.warning(f"[M3-TRAJ] trajectory[{idx}] 缺少 content")
            continue

        if isinstance(content, list):
            for item in content:
                if not isinstance(item, dict):
                    continue
                item_type = item.get("type")
                if item_type == "tool_use":
                    tname = item.get("name")
                    if tname:
                        tool_use_ids.add(tname)
                        logger.debug(f"[M3-TRAJ] 检测到 tool_use: name={tname}")
                elif item_type == "tool_result":
                    tid = item.get("tool_use_id")
                    if tid:
                        tool_result_ids.add(tid)
                        logger.debug(f"[M3-TRAJ] 检测到 tool_result: tool_use_id={tid}")

    if "user" not in roles:
        ERROR_MESSAGES.append(f"[M3-ROLE] trajectory 中缺少 user 消息 (roles={roles})")
        report.add("M3-ROLE", "trajectory 中缺少 user 消息")
        logger.warning(f"[M3-ROLE] trajectory 中缺少 user 消息 (roles={roles})")
    if "assistant" not in roles:
        ERROR_MESSAGES.append(f"[M3-ROLE] trajectory 中缺少 assistant 消息 (roles={roles})")
        report.add("M3-ROLE", "trajectory 中缺少 assistant 消息")
        logger.warning(f"[M3-ROLE] trajectory 中缺少 assistant 消息 (roles={roles})")

    orphans = tool_result_ids - tool_use_ids
    if orphans:
        sample = list(orphans)[:5]
        report.add(
            "M3-TOOL",
            f"tool_result 引用了不存在的 tool_use name ({len(orphans)} 个): {sample}",
            "warning",
        )
        ERROR_MESSAGES.append(f"[M3-TOOL] tool_result 引用了 id: {sample}")
        logger.warning(f"[M3-TOOL] tool_result 引用了不存在的 tool_use id: {sample}")
    else:
        logger.debug(f"[M3-TOOL] tool_use 和 tool_result NAME 匹配正常")






# 初始状态验证（需要 Docker）

def check_initial_state(project_dir: Path, docker_image: str) -> ModuleReport:
    """验证容器内的初始状态。"""
    logger.info(f"[M6] 开始检查初始状态")
    report = ModuleReport(name="M6-初始状态验证")
    global ERROR_MESSAGES
    
    if not ENABLE_M6_INITIAL_STATE:
        return _skipped_report(report.name, "M6 已关闭")

    if not docker_image:
        report.add("M6-SKIP", "未指定 --image，跳过容器内初始状态验证", "info")
        logger.warning(f"[M6] 未指定 Docker 镜像，跳过检查")
        return report

    json_path = project_dir / "trajectory.json"
    records, _ = load_trajectory_json(json_path, force_json_format=not ENABLE_JSON_FORMAT)
    if not records:
        ERROR_MESSAGES.append(f"[M6-FILE] trajectory.json 不存在或为空")
        report.add("M6-SKIP", "无法加载 trajectory.json，跳过检查", "info")
        logger.warning(f"[M6] 无法加载 trajectory.json，跳过检查")
        return report

    record = records[0]
    git_ctx = _extract_git_context(record)
    initial_state = git_ctx.get("initial_state", {}) if git_ctx else {}

    if not isinstance(initial_state, dict) or not initial_state:
        ERROR_MESSAGES.append(f"[M6-FILE] initial_state 为空或格式异常")
        report.add("M6-SKIP", "initial_state 为空或格式异常，跳过检查", "info")
        logger.warning(f"[M6] initial_state 为空或格式异常，跳过检查")
        return report

    logger.info(f"[M6] initial_state 包含 {len(initial_state)} 个文件")
    
    repo_path = get_repo_path(project_dir)
    logger.info(f"[M6] 仓库路径：{repo_path}")

    container_id = _start_container(docker_image, report)
    if not container_id:
        ERROR_MESSAGES.append(f"[M6-CONTAINER] 容器启动失败")
        report.add("M6-SKIP", "容器启动失败，跳过检查", "info")
        logger.error(f"[M6] 容器启动失败，终止检查")
        return report

    try:
        match_count = 0
        mismatch_count = 0
        missing_count = 0

        for filepath, annotated_content in initial_state.items():
            clean_path = re.sub(r"^/?testbed/[^/]+/", "", filepath)
            full_path = f"{repo_path}/{clean_path}"
            
            logger.debug(f"[M6] 检查文件：{clean_path}")

            ok, actual_content = docker_exec(
                container_id, f"cat '{full_path}'", timeout=10,
            )

            if not ok:
                missing_count += 1
                ERROR_MESSAGES.append(f"[M6-FILE] 容器内文件不存在：{clean_path}")
                report.add("M6-MISSING", f"容器内文件不存在：{clean_path}", "error")
                logger.warning(f"[M6] 文件不存在：{clean_path}")
                continue

            annotated_stripped = annotated_content.rstrip()
            actual_stripped = actual_content.rstrip()

            if annotated_stripped == actual_stripped:
                match_count += 1
                logger.debug(f"[M6] ✓ 文件一致：{clean_path}")
            else:
                mismatch_count += 1
                report.add(
                    "M6-MISMATCH",
                    f"文件内容不一致：{clean_path}",
                    "error",
                )
                logger.warning(f"[M6] ✗ 文件不一致：{clean_path}")

        total = match_count + mismatch_count + missing_count
        if total > 0:
            has_failure = (mismatch_count > 0 or missing_count > 0)
            status = "✗" if has_failure else "✓"
            severity = "error" if has_failure else "info"
            
            report.add(
                "M6-SUMMARY",
                f"初始状态验证：{match_count}/{total} 文件完全一致 "
                f"，{mismatch_count} 不一致，{missing_count} 缺失",
                severity,
            )
            
            if has_failure:
                ERROR_MESSAGES.append(
                    f"[M6-FILE] 初始状态验证：{match_count}/{total} 文件完全一致 "
                    f"，{mismatch_count} 不一致，{missing_count} 缺失"
                )
            
            logger.info(f"[M6] {status} 验证完成：{match_count}/{total} 完全一致, {mismatch_count} 不一致，{missing_count} 缺失")
    finally:
        _stop_container(container_id)
        logger.debug(f"[M6] 容器已停止")

    logger.info(f"[M6] 初始状态验证完成")
    return report


def _extract_git_context(record: dict) -> dict | None:
    instance = record.get("instance")
    if isinstance(instance, dict):
        gc = instance.get("git_context")
        if isinstance(gc, dict):
            return gc
    gc = record.get("git_context")
    return gc if isinstance(gc, dict) else None


def _start_container(image: str, report: ModuleReport) -> str | None:
    """启动 Docker 容器。"""
    global ERROR_MESSAGES
    logger.info(f"[Docker] 启动容器，镜像：{image}")
    try:
        cmd = ["docker", "run", "-d", "--rm", image, "sleep", "3600"]
        logger.debug(f"[Docker] 执行命令：{' '.join(cmd)}")
        
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace"
        )
        
        if result.returncode != 0:
            ERROR_MESSAGES.append(f"[M6-CONTAINER] 启动容器失败：{result.stderr.strip()}")
            error_msg = f"启动容器失败：{result.stderr.strip()}"
            report.add("M6-DOCKER", error_msg)
            logger.error(f"[Docker] {error_msg}")
            return None
        
        container_id = result.stdout.strip()
        logger.info(f"[Docker] 容器启动成功，ID: {container_id[:12]}")
        return container_id
    
    except subprocess.TimeoutExpired as exc:
        ERROR_MESSAGES.append(f"[M6-CONTAINER] 启动容器超时：{exc}")
        error_msg = f"Docker 操作超时：{exc}"
        report.add("M6-DOCKER", error_msg)
        logger.error(f"[Docker] {error_msg}")
        return None
    except FileNotFoundError as exc:
        ERROR_MESSAGES.append(f"[M6-CONTAINER] 启动容器失败：{exc}")
        error_msg = f"Docker 未找到：{exc}"
        report.add("M6-DOCKER", error_msg)
        logger.error(f"[Docker] {error_msg}")
        return None


def _stop_container(container_id: str) -> None:
    """停止 Docker 容器。"""
    global ERROR_MESSAGES
    logger.debug(f"[Docker] 停止容器：{container_id[:12]}")
    try:
        result = subprocess.run(
            ["docker", "stop", container_id],
            capture_output=True, timeout=30,
        )
        if result.returncode == 0:
            logger.debug(f"[Docker] 容器已停止")
        else:
            ERROR_MESSAGES.append(f"[M6-CONTAINER] 停止容器失败：{result.stderr.strip()}")
            logger.warning(f"[Docker] 停止容器失败：{result.stderr.strip()}")
    except subprocess.TimeoutExpired as exc:
        ERROR_MESSAGES.append(f"[M6-CONTAINER] 停止容器超时：{exc}")
        logger.warning(f"[Docker] 停止容器超时")
    except FileNotFoundError as exc:
        ERROR_MESSAGES.append(f"[M6-CONTAINER] 停止容器失败：{exc}")
        logger.warning(f"[Docker] Docker 未找到")



# 回归验证（需要 Docker）

def run_verification(project_dir: Path, docker_image: str) -> ModuleReport:
    """运行回归验证。"""
    global ERROR_MESSAGES
    logger.info(f"[M7] 开始回归验证")
    report = ModuleReport(name="M7-回归验证")
    
    if not ENABLE_M7_VERIFICATION:
        return _skipped_report(report.name, "M7 已关闭")

    if not docker_image:
        report.add("M7-SKIP", "未指定 --image，跳过回归验证", "info")
        logger.warning(f"[M7] 未指定 Docker 镜像，跳过验证")
        return report

    # 查找 verification 脚本
    verification_script = None
    for name in VERIFICATION_SCRIPT_NAMES:
        candidate = project_dir / name
        if candidate.is_file():
            verification_script = candidate
            logger.debug(f"[M7] 找到 verification 脚本：{name}")
            break

    if verification_script is None:
        report.add("M7-SKIP", "未找到 verification 脚本，跳过回归验证", "info")
        logger.warning(f"[M7] 未找到 verification 脚本 (搜索：{VERIFICATION_SCRIPT_NAMES})，跳过验证")
        return report
    # 构建挂载参数
    mount_args = [
        "-v", f"{verification_script}:/testbed/run_verification.py",
    ]
    mounted_files = []
    for filename in VERIFICATION_MOUNT_FILES:
        filepath = project_dir / filename
        if filepath.is_file():
            mount_args += ["-v", f"{filepath}:/testbed/{filename}"]
            mounted_files.append(filename)
            logger.debug(f"[M7] 挂载文件：{filename}")
        else:
            ERROR_MESSAGES.append(f"[M7-DOCKER] 文件不存在，无法挂载：{filename}")
            logger.warning(f"[M7] 文件不存在，无法挂载：{filename}")

    base_verification_cmd = "source ~/.bashrc && " + wrap_with_optional_conda(
        project_dir,
        "cd /testbed && python run_verification.py",
    )
    js_verification_cmd = "source ~/.bashrc && " + wrap_with_optional_conda(
        project_dir,
        "export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \. \"$NVM_DIR/nvm.sh\" && cd /testbed && python run_verification.py",
    )

    cmd = [
        "docker", "run","-it" ,"--rm",
        *mount_args,
        docker_image,
        "bash", "-i", "-c", base_verification_cmd,
    ]
    cmd1 = [
        "docker", "run","-it" ,"--rm",
        *mount_args,
        docker_image,
        "bash", "-i", "-c", base_verification_cmd,
    ]
    js_cmd = [
        "docker", "run","-it" ,"--rm",
        *mount_args,
        docker_image,
        "bash", "-i", "-c", js_verification_cmd,
    ]
    logger.info(f"[M7] 执行 Docker 命令")
    logger.debug(f"[M7] 命令：{' '.join(cmd)}")
    logger.debug(f"[M7] 挂载文件：{mounted_files}")

    try:
        if "js" in LANGUAGE or "JS" in LANGUAGE or "javascript" in LANGUAGE or "JavaScript" in LANGUAGE:
            cmd = js_cmd
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        if result.returncode != 0:
            cmd = cmd1
            result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
            )
        logger.debug(f"[M7] 返回码：{result.returncode}")
        
        if result.stdout.strip():
            logger.info(f"[M7] STDOUT:\n{result.stdout}")
        if result.stderr.strip():
            logger.warning(f"[M7] STDERR:\n{result.stderr}")

        if result.returncode == 0:
            report.add("M7-PASS", "回归验证通过", "info")
            logger.info(f"[M7] ✓ 回归验证通过")
        else:
            report.add(
                "M7-FAIL",
                f"回归验证失败 (exit code {result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M7-FAIL] 回归验证失败 (exit code {result.returncode})")
            logger.error(f"[M7] ✗ 回归验证失败 (exit code {result.returncode})")
            
            stderr_tail = "\n".join(result.stderr.strip().splitlines()[-20:])
            stdout_tail = "\n".join(result.stdout.strip().splitlines()[-20:])
            if stderr_tail:
                report.add("M7-DETAIL", f"stderr: {stderr_tail}", "info")
                logger.error(f"[M7] 错误输出 (最后 20 行):\n{stderr_tail}")
            if stdout_tail:
                report.add("M7-DETAIL", f"stdout: {stdout_tail}", "info")
                logger.info(f"[M7] 标准输出 (最后 20 行):\n{stdout_tail}")

    except subprocess.TimeoutExpired:
        error_msg = f"回归验证超时 (>{VERIFICATION_TIMEOUT}s)"
        error_msg = f"回归验证超时 (>{VERIFICATION_TIMEOUT}s)"
        report.add("M7-TIMEOUT", error_msg)
        logger.error(f"[M7] {error_msg}")
    except FileNotFoundError:
        ERROR_MESSAGES.append(f"[M7-DOCKER] Docker 未找到")
        error_msg = "Docker 不可用"
        report.add("M7-DOCKER", error_msg)
        logger.error(f"[M7] {error_msg}")

    logger.info(f"[M7] 回归验证完成")
    return report

# 提取test.patch中的测试文件
def extract_test_files(test_patch: Path) -> list[Path]:
    """从 test.patch 中提取测试文件路径，跳过纯删除的文件。"""
    test_files = []
    deleted_file = None
    
    with test_patch.open("r", encoding="utf-8") as f:
        for line in f:
            # 记录被删除的文件（用于日志）
            if line.startswith("--- a/"):
                deleted_file = line[6:].strip()
            
            # 跳过删除文件的情况（+++ /dev/null）
            if line.startswith("+++ /dev/null"):
                if deleted_file:
                    logger.debug(f"[M8] 跳过已删除的测试文件：{deleted_file}")
                deleted_file = None
                continue
            
            # 提取测试文件路径，忽略不以[py,java,js,ts,cpp,go]结尾的文件
            if line.startswith("+++ b/"):
                file_path = line[6:].strip()
                if file_path.endswith((".py", ".java", ".js", ".ts", ".cpp", ".go")):
                    test_files.append(Path(file_path))
                    logger.debug(f"[M8] 提取测试文件：{file_path}")
                deleted_file = None
    
    logger.info(f"[M8] 从 test.patch 提取了 {len(test_files)} 个测试文件")
    return test_files


# 获取仓库路径（移植自 to_json.py 的 get_repo_path）
def get_repo_path(project_dir: Path) -> str:
    """获取仓库在容器内的绝对路径。
    
    优先级：
    1. 从 setup_repo.sh 中解析 git clone 的目标路径
    2. 从 trajectory.json 的 instance.repo 中提取仓库名
    3. 兜底返回 /testbed
    """
    # 1. 从 setup_repo.sh 中解析
    setup_repo_path = project_dir / "setup_repo.sh"
    if setup_repo_path.is_file():
        for raw_line in load_text(setup_repo_path).splitlines():
            line = raw_line.strip()
            if not line.startswith("git clone"):
                continue
            target = line.split()[-1].strip()
            if target.startswith("/testbed/"):
                return target.rstrip("/")
            break

    # 2. 从 trajectory.json 回退
    json_path = project_dir / "trajectory.json"
    if json_path.is_file():
        content_json = load_text(json_path).strip()
        if content_json:
            try:
                record = json.loads(content_json)
            except json.JSONDecodeError:
                record = None
            if isinstance(record, dict):
                pass  # use as-is
            elif isinstance(record, list) and record and isinstance(record[0], dict):
                record = record[0]
            else:
                record = None

            if record:
                instance = record.get("instance", {})
                if isinstance(instance, dict):
                    repo = instance.get("repo", "")
                    if isinstance(repo, str) and repo.strip():
                        repo_name = repo.rstrip("/").split("/")[-1]
                        if repo_name:
                            return f"/testbed/{repo_name}"

    # 3. 兜底
    return "/testbed"


# 从run_verification.py中提取项目路径，该脚本的项目路径是一个静态常量REPO_PATH
def extract_project_path(verification_script: Path) -> str:
    global ERROR_MESSAGES

    """从 verification 脚本中提取项目路径。"""
    with verification_script.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 首先查找 Context.REPO_PATH 的赋值（优先级更高）
    for line in lines:
        if line.strip().startswith("Context.REPO_PATH = "):
            path_str = line.split("=")[1].strip().strip('"\'')
            if path_str:
                return path_str
    
    # 然后查找直接的 REPO_PATH 赋值（但跳过初始化为空的情况）
    for line in lines:
        if line.strip().startswith("REPO_PATH = "):
            path_str = line.split("=")[1].strip().strip('"\'')
            if path_str:  # 只有当值非空时才返回
                return path_str
    
    ERROR_MESSAGES.append(f"[M8-FAIL] 未找到项目路径常量 REPO_PATH")
    raise ValueError("未找到项目路径常量 REPO_PATH")
# 不依赖数据提供的脚本进行回归验证
def run_verification_no_data(project_dir: Path, docker_image: str) -> ModuleReport:

    """运行不依赖脚本的回归验证。"""
    report = ModuleReport(name="M8-不依赖脚本的回归验证")
    if not ENABLE_M8_NO_DATA_VERIFICATION:
        return _skipped_report(report.name, "M8 已关闭")
    logger.info(f"[M8] 启动不依赖脚本的回归验证")
    logger.info(f"[M8] 项目语言：{LANGUAGE}")
    # 忽略大小写
    if "python" in [lang.lower() for lang in LANGUAGE]:
        return py_run_verification_no_data(project_dir, docker_image)
    elif "java" in [lang.lower() for lang in LANGUAGE]:
        return java_run_verification_no_data(project_dir, docker_image)
    elif "c++" in [lang.lower() for lang in LANGUAGE]:
        return cpp_run_verification_no_data(project_dir, docker_image)
    elif "go" in [lang.lower() for lang in LANGUAGE]:
        return go_run_verification_no_data(project_dir, docker_image)
    elif "javascript" in [lang.lower() for lang in LANGUAGE]:
        return js_run_verification_no_data(project_dir, docker_image)
    else:
        ERROR_MESSAGES.append(f"[M8-FAIL] 不支持的项目语言：{LANGUAGE}")
        logger.warning(f"[M8] 不支持的项目语言：{LANGUAGE}")
        return _skipped_report("M8-不依赖脚本的回归验证", f"不支持的项目语言：{LANGUAGE}")

def py_run_verification_no_data(project_dir: Path, docker_image: str) -> ModuleReport:
    global ERROR_MESSAGES
    logger.info(f"[M8] 开始不依赖脚本的回归验证")
    report = ModuleReport(name="M8-不依赖脚本的回归验证")
    if not docker_image:
        report.add("M8-SKIP", "未指定 --image，跳过回归验证", "info")
        logger.warning(f"[M8] 未指定 Docker 镜像，跳过验证")
        return report
    mounted_files = []
    mount_args = []
    for filename in VERIFICATION_MOUNT_FILES:
        filepath = project_dir / filename
        if filepath.is_file():
            mount_args += ["-v", f"{filepath}:/testbed/{filename}"]
            mounted_files.append(filename)
            logger.debug(f"[M8] 挂载文件：{filename}")
        else:
            ERROR_MESSAGES.append(f"[M8-FAIL] 文件不存在，无法挂载：{filename}")
            logger.warning(f"[M8] 文件不存在，无法挂载：{filename}")

    # 将path转换为字符串，且转换为 file1 file2 file3 格式，且file中的\替换为/
    test_files = extract_test_files(project_dir / 'test.patch')
    test_files_str = " ".join([str(file).replace("\\", "/") for file in test_files])
    pytest_cmd = f"if command -v pytest >/dev/null 2>&1; then pytest -vs {test_files_str}; else python -m pytest -vs {test_files_str}; fi"
    # 获取项目路径（已经是字符串）
    repo_path_str = get_repo_path(project_dir)
    cmd1 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"source ~/.bashrc && cd {repo_path_str} && git apply -v ../test.patch && {pytest_cmd}",
        ),
    ]
    cmd2 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"source ~/.bashrc && cd {repo_path_str} && git apply -v ../test.patch && git apply -v ../final.diff && {pytest_cmd}",
        ),
    ]
    logger.info(f"[M8] 执行 Docker 命令")
    logger.debug(f"[M8] 命令：{' '.join(cmd1)}")
    logger.debug(f"[M8] 挂载文件：{mounted_files}")
    try:
        result = subprocess.run(
            cmd1, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        logger.debug(f"[M8] 返回码：{result.returncode}")
        # 记录测试是否有报错，如果有报错，则记录，如果没有报错，则说明回归验证失败，直接返回失败信息：bug复现失败
        if result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{result.stdout}")
        if result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{result.stderr}")

        if result.returncode != 0:
            report.add("M8", "bug已复现", "info")
        
        if result.returncode == 0:
            report.add(
                "M8-FAIL",
                f"bug复现失败 (exit code {result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug复现失败 (exit code {result.returncode})")
            logger.error(f"[M8] ✗ bug复现失败 (exit code {result.returncode})")
            return report
        fix_result = subprocess.run(
            cmd2, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        logger.debug(f"[M8] 返回码：{fix_result.returncode}")
        if fix_result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{fix_result.stdout}")
        if fix_result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{fix_result.stderr}")

        if fix_result.returncode == 0:
            report.add("M8-FIX", "bug修复成功", "info")
            return report
        if fix_result.returncode != 0:
            report.add(
                "M8-FIX-FAIL",
                f"bug修复失败 (exit code {fix_result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (exit code {fix_result.returncode})")
            logger.error(f"[M8] ✗ bug修复失败 (exit code {fix_result.returncode})")
            msg = f"bug修复失败 (exit code {fix_result.returncode})"
            return report
    except subprocess.TimeoutExpired:
        report.add(
            "M8-FAIL",
            f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)",
        )
        ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        logger.error(f"[M8] ✗ bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        msg = f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)"
        return report
    
def java_run_verification_no_data(project_dir: Path, docker_image: str) -> ModuleReport:
    # ERROR: 处理 checkstyle__checkstyle-18384 时出错: [Errno 13] Permission denied: 'C:\\Users\\user\\test\\verify\\newAgentCoding\\质检脚本测试\\checkstyle__checkstyle-18384'
    # 实现 Java 不依赖脚本的回归验证
    global ERROR_MESSAGES
    logger.info(f"[M8] 执行 Java 不依赖脚本的回归验证")
    report = ModuleReport("M8-JAVA")
    if not docker_image:
        report.add("M8-SKIP", "未指定 --image，跳过回归验证", "info")
        logger.warning(f"[M8] 未指定 Docker 镜像，跳过验证")
        return report
    mounted_files = []
    mount_args = []
    for filename in VERIFICATION_MOUNT_FILES:
        filepath = project_dir / filename
        if filepath.is_file():
            mount_args += ["-v", f"{filepath}:/testbed/{filename}"]
            mounted_files.append(filename)
            logger.debug(f"[M8] 挂载文件：{filename}")
        else:
            ERROR_MESSAGES.append(f"[M8-FAIL] 文件不存在，无法挂载：{filename}")
            logger.warning(f"[M8] 文件不存在，无法挂载：{filename}")
    test_files = []
    test_modules = []
    # 获取Java的测试文件
    test_patch_path = project_dir / 'test.patch'
    test_files = extract_test_files(test_patch_path)
    # 提取测试类名,java的文件路径一般是xxxx/xxxx/xxxx/xxxx/测试类名.java
    for test_file in test_files:
        # 如果类名包含Annotation，则跳过
        if "Annotation" in str(test_file).replace("\\", "/").split("/")[-1].split(".")[0]:
            continue
        else:
            test_module = str(test_file).replace("\\", "/").split("/")[-1].split(".")[0]
            test_modules.append(test_module)
    # 将测试模块转换为字符串，用逗号分隔
    test_modules_str = ",".join(test_modules)
    report.add("M8-TEST", f"运行测试模块：{test_modules_str}", "info")
    logger.info(f"[M8] 运行测试模块：{test_modules_str}")
    # 获取项目路径（已经是字符串）
    repo_path = get_repo_path(project_dir)
    cmd1 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"source ~/.bashrc && cd {repo_path} && git apply -v ../test.patch && mvn clean compile && mvn test -Dtest={test_modules_str}",
        ),
    ]
    logger.info(f"[M8] 执行 Docker 命令：{cmd1}")
    cmd2 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"source ~/.bashrc && cd {repo_path} && git apply -v ../test.patch && git apply -v ../final.diff && mvn clean compile && mvn test -Dtest={test_modules_str}",
        ),
    ]
    logger.info(f"[M8] 执行 Docker 命令：{cmd2}")
    try:
        result = subprocess.run(
            cmd1, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        logger.debug(f"[M8] 返回码：{result.returncode}")
        # 记录测试是否有报错，如果有报错，则记录，如果没有报错，则说明回归验证失败，直接返回失败信息：bug复现失败
        if result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{result.stdout}")
        if result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{result.stderr}")

        if result.returncode != 0:
            report.add("M8", "bug已复现", "info")
        
        if result.returncode == 0:
            report.add(
                "M8-FAIL",
                f"bug复现失败 (exit code {result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug复现失败 (exit code {result.returncode})")
            logger.error(f"[M8] ✗ bug复现失败 (exit code {result.returncode})")
            return report
        fix_result = subprocess.run(
            cmd2, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        logger.debug(f"[M8] 返回码：{fix_result.returncode}")
        if fix_result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{fix_result.stdout}")
        if fix_result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{fix_result.stderr}")

        if fix_result.returncode == 0:
            report.add("M8-FIX", "bug修复成功", "info")
            return report
        if fix_result.returncode != 0:
            report.add(
                "M8-FIX-FAIL",
                f"bug修复失败 (exit code {fix_result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (exit code {fix_result.returncode})")
            logger.error(f"[M8] ✗ bug修复失败 (exit code {fix_result.returncode})")
            return report
    except subprocess.TimeoutExpired:
        report.add(
            "M8-FAIL",
            f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)",
        )
        ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        logger.error(f"[M8] ✗ bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        msg = f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)"
        return report


def cpp_run_verification_no_data(project_dir: Path, docker_image: str) -> ModuleReport:
    # TODO 实现 C++ 不依赖脚本的回归验证
    global ERROR_MESSAGES
    logger.info(f"[M8] 执行 C++ 不依赖脚本的回归验证")
    report = ModuleReport("M8-CPP")
    if not docker_image:
        report.add("M8-SKIP", "未指定 --image，跳过回归验证", "info")
        logger.warning(f"[M8] 未指定 Docker 镜像，跳过验证")
        return report
    mounted_files = []
    mount_args = []
    for filename in VERIFICATION_MOUNT_FILES:
        filepath = project_dir / filename
        if filepath.is_file():
            mount_args += ["-v", f"{filepath}:/testbed/{filename}"]
            mounted_files.append(filename)
            logger.debug(f"[M8] 挂载文件：{filename}")
        else:
            logger.warning(f"[M8] 文件不存在，无法挂载：{filename}")
    repo_path = get_repo_path(project_dir)
    cmd1 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"source ~/.bashrc && cd {repo_path} && git apply -v ../test.patch && cd ./build && cmake --build . && ctest ",
        ),
    ]
    logger.info(f"[M8] 执行 Docker 命令：{cmd1}")
    cmd2 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"source ~/.bashrc && cd {repo_path} && git apply -v ../test.patch && git apply -v ../final.diff && cd ./build && cmake --build . && ctest ",
        ),
    ]
    logger.info(f"[M8] 执行 Docker 命令：{cmd2}")
    try:
        result = subprocess.run(
            cmd1, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        logger.debug(f"[M8] 返回码：{result.returncode}")
        # 记录测试是否有报错，如果有报错，则记录，如果没有报错，则说明回归验证失败，直接返回失败信息：bug复现失败
        if result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{result.stdout}")
        if result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{result.stderr}")

        if result.returncode != 0:
            report.add("M8", "bug已复现", "info")
        
        if result.returncode == 0:
            report.add(
                "M8-FAIL",
                f"bug复现失败 (exit code {result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug复现失败 (exit code {result.returncode})")
            logger.error(f"[M8] ✗ bug复现失败 (exit code {result.returncode})")
            return report
        fix_result = subprocess.run(
            cmd2, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        logger.debug(f"[M8] 返回码：{fix_result.returncode}")
        if fix_result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{fix_result.stdout}")
        if fix_result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{fix_result.stderr}")

        if fix_result.returncode == 0:
            report.add("M8-FIX", "bug修复成功", "info")
            return report
        if fix_result.returncode != 0:
            report.add(
                "M8-FIX-FAIL",
                f"bug修复失败 (exit code {fix_result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (exit code {fix_result.returncode})")
            logger.error(f"[M8] ✗ bug修复失败 (exit code {fix_result.returncode})")
            return report
    except subprocess.TimeoutExpired:
        report.add(
            "M8-FAIL",
            f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)",
        )
        ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        logger.error(f"[M8] ✗ bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        msg = f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)"
        return report

def go_run_verification_no_data(project_dir: Path, docker_image: str) -> ModuleReport:
    global ERROR_MESSAGES
    logger.info(f"[M8] 执行 Go 不依赖脚本的回归验证")
    report = ModuleReport("M8-GO")
    if not docker_image:
        report.add("M8-SKIP", "未指定 --image，跳过回归验证", "info")
        logger.warning(f"[M8] 未指定 Docker 镜像，跳过验证")
        return report
    mounted_files = []
    mount_args = []
    for filename in VERIFICATION_MOUNT_FILES:
        filepath = project_dir / filename
        if filepath.is_file():
            mount_args += ["-v", f"{filepath}:/testbed/{filename}"]
            mounted_files.append(filename)
            logger.debug(f"[M8] 挂载文件：{filename}")
        else:
            logger.warning(f"[M8] 文件不存在，无法挂载：{filename}")
    repo_path = get_repo_path(project_dir)
    cmd1 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"source ~/.bashrc && cd {repo_path} && git apply -v ../test.patch && go build -o test && go test ./",
        ),
    ]
    logger.info(f"[M8] 执行 Docker 命令：{cmd1}")
    cmd2 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"source ~/.bashrc && cd {repo_path} && git apply -v ../test.patch && git apply -v ../final.diff && go build -o test && go test ./",
        ),
    ]
    logger.info(f"[M8] 执行 Docker 命令：{cmd2}")
    try:
        result = subprocess.run(
            cmd1, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        logger.debug(f"[M8] 返回码：{result.returncode}")
        # 记录测试是否有报错，如果有报错，则记录，如果没有报错，则说明回归验证失败，直接返回失败信息：bug复现失败
        if result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{result.stdout}")
        if result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{result.stderr}")

        if result.returncode != 0:
            report.add("M8", "bug已复现", "info")
        
        if result.returncode == 0:
            report.add(
                "M8-FAIL",
                f"bug复现失败 (exit code {result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug复现失败 (exit code {result.returncode})")
            logger.error(f"[M8] ✗ bug复现失败 (exit code {result.returncode})")
            return report
        fix_result = subprocess.run(
            cmd2, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
            encoding="utf-8", errors="replace"
        )
        logger.debug(f"[M8] 返回码：{fix_result.returncode}")
        if fix_result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{fix_result.stdout}")
        if fix_result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{fix_result.stderr}")

        if fix_result.returncode == 0:
            report.add("M8-FIX", "bug修复成功", "info")
            return report
        if fix_result.returncode != 0:
            report.add(
                "M8-FIX-FAIL",
                f"bug修复失败 (exit code {fix_result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (exit code {fix_result.returncode})")
            logger.error(f"[M8] ✗ bug修复失败 (exit code {fix_result.returncode})")
            return report
    except subprocess.TimeoutExpired:
        report.add(
            "M8-FAIL",
            f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)",
        )
        ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        logger.error(f"[M8] ✗ bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        msg = f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)"
        return report

def js_cmd_run(cmd):
    result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=VERIFICATION_TIMEOUT,
                encoding="utf-8", errors="replace"
            )
    return result


def js_run_verification_no_data(project_dir: Path, docker_image: str) -> ModuleReport:
    # TODO 实现 JavaScript 不依赖脚本的回归验证
    global ERROR_MESSAGES
    logger.info(f"[M8] 开始不依赖脚本的回归验证")
    report = ModuleReport(name="M8-不依赖脚本的回归验证")
    if not docker_image:
        report.add("M8-SKIP", "未指定 --image，跳过回归验证", "info")
        logger.warning(f"[M8] 未指定 Docker 镜像，跳过验证")
        return report
    mounted_files = []
    mount_args = []
    for filename in VERIFICATION_MOUNT_FILES:
        filepath = project_dir / filename
        if filepath.is_file():
            mount_args += ["-v", f"{filepath}:/testbed/{filename}"]
            mounted_files.append(filename)
            logger.debug(f"[M8] 挂载文件：{filename}")
        else:
            ERROR_MESSAGES.append(f"[M8-FAIL] 文件不存在，无法挂载：{filename}")
            logger.warning(f"[M8] 文件不存在，无法挂载：{filename}")

    # 将path转换为字符串，且转换为 file1 file2 file3 格式，且file中的\替换为/
    test_files = extract_test_files(project_dir / 'test.patch')
    test_files_str = " ".join([str(file).replace("\\", "/") for file in test_files])
    # 获取项目路径（已经是字符串）
    repo_path_str = get_repo_path(project_dir)
    cmd1 = [
        "docker", "run", "-it", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \. \"$NVM_DIR/nvm.sh\" && cd {repo_path_str} && git apply -v ../test.patch && source ~/.bashrc && npx mocha {test_files_str}",
        ),
    ]
    cmd1_without_env = [
        "docker", "run", "-it", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"cd {repo_path_str} && git apply -v ../test.patch && source ~/.bashrc && npx mocha {test_files_str}",
        ),
    ]
    cmd1_jest = [
        "docker", "run", "-it", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \. \"$NVM_DIR/nvm.sh\" && cd {repo_path_str} && git apply -v ../test.patch && source ~/.bashrc && npx jest {test_files_str}",
        ),
    ]
    cmd1_jest_without_env= [
        "docker", "run", "-it", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"cd {repo_path_str} && git apply -v ../test.patch && source ~/.bashrc && npx jest {test_files_str}",
        ),
    ]
    
    cmd2 = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \. \"$NVM_DIR/nvm.sh\" && cd {repo_path_str} && git apply -v ../test.patch && git apply -v ../final.diff && source ~/.bashrc && npx mocha {test_files_str}",
        ),
    ]
    cmd2_without_env = [
        "docker", "run", "-it", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"cd {repo_path_str} && git apply -v ../test.patch && git apply -v ../final.diff && source ~/.bashrc && npx mocha {test_files_str}",
        ),
    ]
    cmd2_jest = [
        "docker", "run", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"export NVM_DIR=\"$HOME/.nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \. \"$NVM_DIR/nvm.sh\" && cd {repo_path_str} && git apply -v ../test.patch && git apply -v ../final.diff && source ~/.bashrc && npx jest {test_files_str}",
        ),
    ]
    cmd2_jest_without_env= [
        "docker", "run", "-it", "--rm",
        *mount_args,
        docker_image,
        "bash", "-c", wrap_with_optional_conda(
            project_dir,
            f"cd {repo_path_str} && git apply -v ../test.patch && git apply -v ../final.diff && source ~/.bashrc && npx jest {test_files_str}",
        ),
    ]
    logger.info(f"[M8] 执行 Docker 命令")
    logger.debug(f"[M8] 命令：{' '.join(cmd1)}")
    logger.debug(f"[M8] 挂载文件：{mounted_files}")
    try:
        result = js_cmd_run(cmd1)
        logger.debug(f"docker_cmd1: {' '.join(cmd1)}")
        print(f"docker_cmd1: {' '.join(cmd1)}")
        logger.debug(f"[M8] 返回码：{result.returncode}")
        # 记录测试是否有报错，如果有报错，则记录，如果没有报错，则说明回归验证失败，直接返回失败信息：bug复现失败
        if result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{result.stdout}")
        if result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{result.stderr}")

        if result.returncode != 0:
            report.add("M8", "bug已复现", "info")
        
        if result.returncode == 0:
            report.add(
                "M8-FAIL",
                f"bug复现失败 (exit code {result.returncode})",
            )
            ERROR_MESSAGES.append(f"[M8-FAIL] bug复现失败 (exit code {result.returncode})")
            logger.error(f"[M8] ✗ bug复现失败 (exit code {result.returncode})")
            return report
        fix_result = js_cmd_run(cmd2)
        print(f"docker_cmd2: {' '.join(cmd2)}")
        logger.debug(f"docker_cmd2: {' '.join(cmd2)}")
        logger.debug(f"[M8] 返回码：{fix_result.returncode}")
        if fix_result.stdout.strip():
            logger.info(f"[M8] STDOUT:\n{fix_result.stdout}")
        if fix_result.stderr.strip():
            logger.warning(f"[M8] STDERR:\n{fix_result.stderr}")

        if fix_result.returncode == 0:
            report.add("M8-FIX", "bug修复成功", "info")
            return report
        if fix_result.returncode != 0:
            # TODO :需要处理多种node安装情况
            jest_result = js_cmd_run(cmd1_jest)
            print(f"docker_cmd1_jest: {' '.join(cmd1_jest)}")
            logger.debug(f"docker_cmd1_jest: {' '.join(cmd1_jest)}")
            logger.debug(f"[M8] 返回码：{jest_result.returncode}")
            if jest_result.returncode != 0:
                report.add(
                    "M8-JEST-BUG-REPRODUCED",
                    f"bug已复现 (exit code {jest_result.returncode})","info"
                )
            else:
                report.add(
                "M8-FAIL",
                f"bug复现失败 (exit code {result.returncode})",
                )
                ERROR_MESSAGES.append(f"[M8-FAIL] bug复现失败 (exit code {jest_result.returncode})")
                logger.error(f"[M8] ✗ bug复现失败 (exit code {jest_result.returncode})")
                return report
            jest_fix_result = js_cmd_run(cmd2_jest)
            print(f"docker_cmd2_jest: {' '.join(cmd2_jest)}")
            if jest_fix_result.returncode != 0:
                # 处理另一种node安装情况
                result = js_cmd_run(cmd1_without_env)
                print(f"docker_cmd1_without_env: {' '.join(cmd1_without_env)}")
                logger.debug(f"[M8] 返回码：{result.returncode}")
                if result.stdout.strip():
                    logger.info(f"[M8] STDOUT:\n{result.stdout}")
                if result.stderr.strip():
                    logger.warning(f"[M8] STDERR:\n{result.stderr}")
                if result.returncode != 0:
                    report.add(
                        "M8-BUG-REPRODUCED",
                        f"bug已复现 (exit code {result.returncode})","info"
                    )
                else:
                    report.add(
                        "M8-FAIL",
                        f"bug复现失败 (exit code {result.returncode})",
                    )
                    ERROR_MESSAGES.append(f"[M8-FAIL] bug复现失败 (exit code {result.returncode})")
                    logger.error(f"[M8] ✗ bug复现失败 (exit code {result.returncode})")
                    return report
                fix_result = js_cmd_run(cmd2_without_env)
                if fix_result.returncode == 0:
                    report.add("M8-FIX", "bug修复成功", "info")
                    return report
                else:
                    jest_result = js_cmd_run(cmd1_jest_without_env)
                    if jest_result.returncode != 0:
                        report.add(
                            "M8-JEST-BUG-REPRODUCED",
                            f"bug已复现 (exit code {jest_result.returncode})","info"
                        )
                    else:
                        report.add(
                            "M8-FAIL",
                            f"bug复现失败 (exit code {jest_result.returncode})",
                        )
                        ERROR_MESSAGES.append(f"[M8-FAIL] bug复现失败 (exit code {jest_result.returncode})")
                        logger.error(f"[M8] ✗ bug复现失败 (exit code {jest_result.returncode})")
                        return report
                    jest_fix_result = js_cmd_run(cmd2_jest_without_env)
                    if jest_fix_result.returncode == 0:
                        report.add("M8-FIX", "bug修复成功", "info")
                        return report
                    else:
                        report.add(
                            "M8-FIX-FAIL",
                            f"bug修复失败 (exit code {jest_fix_result.returncode})",
                        )
                        ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (exit code {jest_fix_result.returncode})")
                        logger.error(f"[M8] ✗ bug修复失败 (exit code {jest_fix_result.returncode})")
                        return report

            else:
                report.add(
                    "M8-FIX", "bug修复成功", "info"
                )
                return report
    except subprocess.TimeoutExpired:
        report.add(
            "M8-FAIL",
            f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)",
        )
        ERROR_MESSAGES.append(f"[M8-FAIL] bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        logger.error(f"[M8] ✗ bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)")
        msg = f"bug修复失败 (超时 {VERIFICATION_TIMEOUT} 秒)"
        return report


def print_report(modules: list[ModuleReport]) -> None:
    """打印控制台报告。"""
    logger.debug("=" * 60)
    logger.debug("生成质检报告")
    
    total_errors = sum(
        sum(1 for i in m.issues if i.severity == "error") for m in modules
    )
    total_warnings = sum(
        sum(1 for i in m.issues if i.severity == "warning") for m in modules
    )

    logger.info(f"\n{'=' * 60}")
    logger.info("User-Agentic 质检报告")
    logger.info(f"{'=' * 60}")

    for mod in modules:
        status = "PASS" if mod.passed else "FAIL"
        error_count = sum(1 for i in mod.issues if i.severity == "error")
        warning_count = sum(1 for i in mod.issues if i.severity == "warning")
        
        logger.info(f"\n  [{status}] {mod.name}  (errors: {error_count}, warnings: {warning_count})")
        
        # 详细记录每个问题
        for issue in mod.issues:
            if issue.severity == "error":
                tag = "  ERROR"
                logger.error(f"    {tag} [{issue.code}] {issue.message}")
            elif issue.severity == "warning":
                tag = "  WARN "
                logger.warning(f"    {tag} [{issue.code}] {issue.message}")
            else:
                tag = "  INFO "
                logger.info(f"    {tag} [{issue.code}] {issue.message}")

    logger.info(f"\n{'=' * 60}")
    logger.info(f"总计：{total_errors} 错误，{total_warnings} 警告")
    overall = "PASS" if total_errors == 0 else "FAIL"
    logger.info(f"最终结果：{overall}")
    logger.info(f"{'=' * 60}")


def save_report(modules: list[ModuleReport], report_path: Path) -> None:
    """保存 JSON 报告。"""
    total_errors = sum(
        sum(1 for i in m.issues if i.severity == "error") for m in modules
    )
    data = {
        "overall": "PASS" if total_errors == 0 else "FAIL",
        "total_errors": total_errors,
        "total_warnings": sum(
            sum(1 for i in m.issues if i.severity == "warning") for m in modules
        ),
        "modules": [m.to_dict() for m in modules],
    }
    
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    
    logger.info(f"\n质检报告已保存到：{report_path}")
    logger.debug(f"[报告] JSON 报告大小：{len(json.dumps(data, ensure_ascii=False))} 字节")


def is_project_dir(d: Path) -> bool:
    """判断是否为项目目录。"""
    if (d / "trajectory.json").is_file():
        logger.debug(f"[目录检测] {d.name} 包含 trajectory.json，是项目目录")
        return True
    json_files = [f for f in d.iterdir() if f.is_file() and f.suffix == ".json" and "__" in f.stem]
    if json_files:
        logger.debug(f"[目录检测] {d.name} 包含 instance JSON: {[f.name for f in json_files]}")
        return True
    logger.debug(f"[目录检测] {d.name} 不是项目目录")
    return False


def find_project_dirs(root: Path) -> list[Path]:
    """查找所有项目目录。"""
    logger.info(f"[目录扫描] 在 {root} 中搜索项目目录")
    dirs = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and is_project_dir(child):
            dirs.append(child)
    
    if dirs:
        logger.info(f"[目录扫描] 找到 {len(dirs)} 个项目目录：{[d.name for d in dirs]}")
    else:
        logger.warning(f"[目录扫描] 未找到任何项目目录")
    return dirs


def _extract_field_paths(obj, prefix="") -> set[str]:
    """递归提取 JSON 对象中所有字段的路径（点号分隔）。"""
    paths = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            paths.add(path)
            paths |= _extract_field_paths(value, path)
    elif isinstance(obj, list) and obj:
        if isinstance(obj[0], dict):
            paths |= _extract_field_paths(obj[0], prefix)
        elif isinstance(obj[0], list):
            paths |= _extract_field_paths(obj[0], prefix)
    return paths


def check_trajectory_field_names(project_dir: Path) -> ModuleReport:
    """检查 trajectory.json 字段名完备性（对比 example）。"""
    logger.info(f"[M9] 开始检查 trajectory.json 字段名完备性")
    report = ModuleReport(name="M9-trajectory字段名完备性")
    global ERROR_MESSAGES
    if not ENABLE_M9_TRAJECTORY_FIELD_NAMES:
        return _skipped_report(report.name, "M9 已关闭")

    example_traj = EXAMPLE_DIR / "trajectory.json"
    if not example_traj.is_file():
        report.add("M9-LOAD", "example/trajectory.json 不存在")
        logger.error("[M9] example/trajectory.json 不存在")
        return report

    task_json_path = project_dir / "trajectory.json"
    if not task_json_path.is_file():
        report.add("M9-LOAD", "trajectory.json 不存在")
        logger.error("[M9] trajectory.json 不存在")
        return report

    example_data = load_json(example_traj)
    if example_data is None:
        report.add("M9-PARSE", "example/trajectory.json 解析失败")
        return report

    task_data = load_json(task_json_path)
    if task_data is None:
        report.add("M9-PARSE", "trajectory.json 解析失败")
        return report

    # 支持 trajectory.json 可能是数组（多条记录）
    if isinstance(task_data, list):
        if len(task_data) == 0:
            report.add("M9-EMPTY", "trajectory.json 为空数组")
            return report
        task_data = task_data[0]
    if isinstance(example_data, list):
        if len(example_data) == 0:
            report.add("M9-EMPTY", "example/trajectory.json 为空数组")
            return report
        example_data = example_data[0]

    example_paths = _extract_field_paths(example_data)
    task_paths = _extract_field_paths(task_data)

    # 排除 initial_state 及其子字段的检查
    # _extract_field_paths 返回点号分隔的全路径（如 instance.git_context.initial_state）
    example_paths = {p for p in example_paths if "initial_state" not in p}
    task_paths = {p for p in task_paths if "initial_state" not in p}

    # 当 agent 为 claude code 时，跳过 coding_agent_system_prompt 和 tools 字段对比
    task_meta = task_data.get("metadata", {}) if isinstance(task_data, dict) else {}
    if task_meta.get("agent") == "claude code":
        logger.info("[M9] agent 为 claude code，跳过 coding_agent_system_prompt 和 tools 字段对比")
        example_paths = {p for p in example_paths
                         if not p.startswith("metadata.coding_agent_system_prompt")
                         and not p.startswith("metadata.tools")}
        task_paths = {p for p in task_paths
                      if not p.startswith("metadata.coding_agent_system_prompt")
                      and not p.startswith("metadata.tools")}

    missing = sorted(example_paths - task_paths)
    if missing:
        missing_str = ", ".join(missing)
        ERROR_MESSAGES.append(f"[M9] 字段完备性缺失：{missing_str}")
        report.add("M9-MISSING", f"字段完备性缺失：{missing_str}")
        logger.error(f"[M9] 字段完备性缺失：{missing_str}")
    else:
        logger.info(f"[M9] 字段名完备性检查通过")

    logger.info(f"[M9] trajectory.json 字段名完备性检查完成")
    return report


def check_system_prompt_similarity(project_dir: Path) -> ModuleReport:
    """检查 coding_agent_system_prompt 与 example 的相似度。"""
    logger.info(f"[M10] 开始检查 system prompt 相似度")
    report = ModuleReport(name="M10-system prompt相似度")
    global ERROR_MESSAGES
    if not ENABLE_M10_SYSTEM_PROMPT:
        return _skipped_report(report.name, "M10 已关闭")

    example_traj = EXAMPLE_DIR / "trajectory.json"
    if not example_traj.is_file():
        report.add("M10-LOAD", "example/trajectory.json 不存在")
        logger.error("[M10] example/trajectory.json 不存在")
        return report

    task_json_path = project_dir / "trajectory.json"
    if not task_json_path.is_file():
        report.add("M10-LOAD", "trajectory.json 不存在")
        logger.error("[M10] trajectory.json 不存在")
        return report

    example_data = load_json(example_traj)
    if example_data is None:
        report.add("M10-PARSE", "example/trajectory.json 解析失败")
        return report

    task_data = load_json(task_json_path)
    if task_data is None:
        report.add("M10-PARSE", "trajectory.json 解析失败")
        return report

    if isinstance(example_data, list):
        example_data = example_data[0] if example_data else {}
    if isinstance(task_data, list):
        task_data = task_data[0] if task_data else {}

    example_meta = example_data.get("metadata", {})
    task_meta = task_data.get("metadata", {})

    # 当 agent 为 claude code 时，跳过 coding_agent_system_prompt 相似度校验
    if task_meta.get("agent") == "claude code":
        logger.info("[M10] agent 为 claude code，跳过 system prompt 相似度校验")
        report.add("M10-SKIP", "agent 为 claude code，跳过校验", "info")
        return report

    example_prompt = example_meta.get("coding_agent_system_prompt", "")
    task_prompt = task_meta.get("coding_agent_system_prompt", "")

    if not example_prompt:
        report.add("M10-EMPTY", "example 中 coding_agent_system_prompt 为空或不存在")
        return report
    if not task_prompt:
        ERROR_MESSAGES.append("[M10] 质检数据中 coding_agent_system_prompt 为空或不存在")
        report.add("M10-EMPTY", "质检数据中 coding_agent_system_prompt 为空或不存在")
        return report

    similarity = SequenceMatcher(None, example_prompt, task_prompt).ratio()
    logger.info(f"[M10] system prompt 相似度：{similarity:.4f}")

    if SYSTEM_PROMPT_SIMILARITY_LOWER_BOUND < similarity < SYSTEM_PROMPT_SIMILARITY_UPPER_BOUND:
        report.add("M10-PASS", f"系统提示词校验通过 (相似度: {similarity:.2%})", "info")
        logger.info(f"[M10] ✓ 系统提示词校验通过 (相似度: {similarity:.2%})")
    else:
        ERROR_MESSAGES.append(f"[M10] 系统提示词校验失败 (相似度: {similarity:.2%}, 期望 > 95% 且 != 100%)")
        report.add("M10-FAIL", f"系统提示词校验失败 (相似度: {similarity:.2%}, 期望 > 95% 且 != 100%)")
        logger.error(f"[M10] ✗ 系统提示词校验失败 (相似度: {similarity:.2%})")

    return report


def find_field_recursively(data, target_field):
    """递归在 JSON 中查找目标字段的值，不管嵌套层级"""
    if isinstance(data, dict):
        if target_field in data:
            return data[target_field]
        for k, v in data.items():
            result = find_field_recursively(v, target_field)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_field_recursively(item, target_field)
            if result is not None:
                return result
    return None


def extract_git_state(initial_state_content):
    """从 initial_state 中提取 git 状态（文件列表+内容），用于后续对比"""
    if not initial_state_content:
        return {}
    files = {}
    if isinstance(initial_state_content, str):
        files["__initial_state__"] = initial_state_content
    elif isinstance(initial_state_content, dict):
        files = initial_state_content
    return files


def apply_patch_and_get_state(diff_path):
    if not diff_path.exists():
        return {}
    try:
        with open(diff_path, "r", encoding="utf-8") as f:
            diff_content = f.read()
        return {"__patched_state__": diff_content}
    except:
        return {}


def calculate_git_state_similarity(initial_state, patched_state):
    if not initial_state or not patched_state:
        return 0.0
    initial_str = str(initial_state)
    patched_str = str(patched_state)
    ratio = SequenceMatcher(None, initial_str, patched_str).ratio()
    return round(ratio * 100, 2)


def check_custom_consistency(project_dir: Path) -> ModuleReport:
    """检查自定义一致性与重合度校验。"""
    logger.info(f"[M11] 开始进行自定义一致性与重合度校验")
    report = ModuleReport(name="M11-自定义一致性校验")
    global ERROR_MESSAGES
    if not ENABLE_M11_CUSTOM_CHECK:
        return _skipped_report(report.name, "M11 已关闭")

    # 1. 校验 run_verification.py 内部是否正确替换为 final.diff
    rv_path = project_dir / "run_verification.py"
    if rv_path.is_file():
        try:
            content = load_text(rv_path)
            content_lines = content.splitlines()
            # 过滤掉注释行
            has_code_patch = any("code.patch" in line.strip() and not line.strip().startswith("#") for line in content_lines)
            has_final = "final.diff" in "".join([l for l in content_lines if not l.strip().startswith("#")])
            
            if has_code_patch:
                report.add("M11-RV-PATCH", "run_verification.py 仍包含 code.patch，未替换为 final.diff", "error")
                ERROR_MESSAGES.append("[M11] run_verification.py 仍包含 code.patch")
                logger.error("[M11] run_verification.py 仍包含 code.patch")
            elif not has_final:
                report.add("M11-RV-DIFF", "run_verification.py 未找到 final.diff，替换不完整", "error")
                ERROR_MESSAGES.append("[M11] run_verification.py 未找到 final.diff")
                logger.error("[M11] run_verification.py 未找到 final.diff")
            else:
                logger.info("[M11] run_verification.py 已经正确替换为 final.diff")
        except Exception as e:
            report.add("M11-RV-READ", f"run_verification.py 读取失败：{e}", "error")
            ERROR_MESSAGES.append(f"[M11] run_verification.py 读取失败: {e}")
            logger.error(f"[M11] run_verification.py 读取失败: {e}")

    # 2. 校验 instance_id 跨文件一致性
    instance_json = find_instance_json(project_dir)
    trajectory_json = project_dir / "trajectory.json"
    
    inst_instance_id = None
    traj_instance_id = None
    
    if instance_json and instance_json.is_file():
        inst_data = load_json(instance_json)
        if isinstance(inst_data, dict):
            inst_instance_id = inst_data.get("instance_id")
            
    if trajectory_json.is_file():
        records, _ = load_trajectory_json(trajectory_json, force_json_format=not ENABLE_JSON_FORMAT)
        if records:
            traj_instance_id = find_field_recursively(records[0], "instance_id")
            
    if inst_instance_id and traj_instance_id:
        if inst_instance_id != traj_instance_id:
            report.add(
                "M11-ID-MISMATCH",
                f"跨文件 instance_id 不一致！instance.json 里为 '{inst_instance_id}'，而 trajectory.json 里为 '{traj_instance_id}'",
                "error",
            )
            ERROR_MESSAGES.append(f"[M11] 跨文件 instance_id 不一致：'{inst_instance_id}' vs '{traj_instance_id}'")
            logger.error(f"[M11] 跨文件 instance_id 不一致：'{inst_instance_id}' vs '{traj_instance_id}'")
        else:
            logger.info(f"[M11] 跨文件 instance_id 一致性校验通过：'{inst_instance_id}'")
    elif inst_instance_id is None and instance_json:
        report.add("M11-ID-MISSING", "未从 instance 配置文件中读取到 instance_id", "error")
        ERROR_MESSAGES.append("[M11] 未从 instance 配置文件中读取到 instance_id")
        logger.error("[M11] 未从 instance 配置文件中读取到 instance_id")
    elif traj_instance_id is None and trajectory_json.is_file():
        report.add("M11-ID-MISSING", "未从 trajectory.json 中读取到 instance_id", "error")
        ERROR_MESSAGES.append("[M11] 未从 trajectory.json 中读取到 instance_id")
        logger.error("[M11] 未从 trajectory.json 中读取到 instance_id")

    # 3. 对比 code.patch 与 final.diff 内容重合度
    p1 = project_dir / "code.patch"
    p2 = project_dir / "final.diff"
    if p1.is_file() and p2.is_file():
        try:
            c1 = p1.read_text(encoding="utf-8", errors="ignore").strip()
            c2 = p2.read_text(encoding="utf-8", errors="ignore").strip()
            ratio = round(SequenceMatcher(None, c1, c2).ratio() * 100, 2)
            report.add("M11-PATCH-SIMILARITY", f"code.patch 与 final.diff 内容重合度：{ratio}%", "info")
            logger.info(f"[M11] code.patch 与 final.diff 内容重合度：{ratio}%")
        except Exception as e:
            logger.warning(f"[M11] 对比 code.patch 与 final.diff 失败：{e}")

    # 4. 校验 initial_state 涉及的文件是否包含 final.diff 中涉及到的所有文件
    def clean_file_path(p: str) -> str:
        p = p.replace("\\", "/").strip("/")
        p = re.sub(r"^(?:a|b)/", "", p)
        p = re.sub(r"^/?testbed/[^/]+/", "", p)
        p = re.sub(r"^testbed/", "", p)
        return p

    def extract_patched_files(patch_path: Path) -> list[str]:
        files = []
        if not patch_path.is_file():
            return files
        try:
            with patch_path.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.startswith("+++ b/"):
                        path_str = line[6:].strip()
                        if path_str != "/dev/null" and path_str:
                            files.append(path_str)
                    elif line.startswith("--- a/"):
                        path_str = line[6:].strip()
                        if path_str != "/dev/null" and path_str and path_str not in files:
                            files.append(path_str)
        except Exception as e:
            logger.warning(f"[M11] 解析 patch 失败: {patch_path}, 错误: {e}")
        return list(set(files))

    if trajectory_json.is_file():
        records, _ = load_trajectory_json(trajectory_json, force_json_format=not ENABLE_JSON_FORMAT)
        if records:
            initial_state_val = find_field_recursively(records[0], "initial_state")
            if initial_state_val and p2.is_file():
                try:
                    initial_state = extract_git_state(initial_state_val)
                    if isinstance(initial_state, dict) and initial_state:
                        patched_files = extract_patched_files(p2)
                        cleaned_diff_files = {clean_file_path(f) for f in patched_files}
                        cleaned_init_files = {clean_file_path(f) for f in initial_state.keys()}
                        
                        missing_files = sorted(list(cleaned_diff_files - cleaned_init_files))
                        if missing_files:
                            report.add(
                                "M11-INIT-MISSING",
                                f"initial_state 缺失了 final.diff 中被修改的某些文件：{', '.join(missing_files)}",
                                "error"
                            )
                            ERROR_MESSAGES.append(f"[M11] initial_state 缺失了 final.diff 中的文件: {missing_files}")
                            logger.error(f"[M11] initial_state 缺失了 final.diff 中的文件: {missing_files}")
                        else:
                            report.add("M11-INIT-COVERAGE", "initial_state 完整包含了 final.diff 涉及的所有文件", "info")
                            logger.info("[M11] initial_state 完整包含了 final.diff 涉及的所有文件")
                except Exception as e:
                    logger.warning(f"[M11] 静态 initial_state 文件包含关系校验失败：{e}")

    logger.info(f"[M11] 自定义一致性校验完成，错误数：{sum(1 for i in report.issues if i.severity == 'error')}")
    return report


def run_checks(project_dir: Path, docker_image: str, report_path: str) -> bool:
    global ERROR_MESSAGES
    """运行所有检查。"""
    reset_runtime_state()
    logger.info("=" * 60)
    logger.info(f"质检目标：{project_dir}")
    if docker_image:
        logger.info(f"Docker 镜像：{docker_image}")
    logger.info("=" * 60)

    modules = [
        check_file_completeness(project_dir),
        check_instance_json(project_dir),
        check_trajectory_json(project_dir),
        check_initial_state(project_dir, docker_image),
        run_verification(project_dir, docker_image),
        run_verification_no_data(project_dir, docker_image),
        check_trajectory_field_names(project_dir),
        check_system_prompt_similarity(project_dir),
        check_custom_consistency(project_dir),
    ]

    print_report(modules)
    if SAVE_JSON_REPORT:
        out = Path(report_path) if report_path else project_dir / "qc_report.json"
        save_report(modules, out)

    all_passed = all(m.passed for m in modules)
    logger.info(f"\n{'=' * 60}")
    if all_passed:
        logger.info("✓ 所有检查通过")
    else:
        failed_modules = [m.name for m in modules if not m.passed]
        logger.error(f"✗ {len(failed_modules)} 个模块检查失败：{failed_modules}")
    logger.info(f"{'=' * 60}")
    
    return all_passed


def main(task_dir: Path,image_name:str,log:str) -> None:
    global ERROR_MESSAGES
# def main() -> None:
    """主函数。"""
    error_msg = []
    overall_error_messages = []
    parser = argparse.ArgumentParser(
        description="User-Agentic 数据集质检脚本",
    )
    parser.add_argument(
        "project_dir",
        nargs="?",
        default=str(task_dir),
        help="项目目录路径 (可选；不传则自动扫描当前目录及其子目录)",
    )
    parser.add_argument(
        "--image",
        default=image_name,
        help="Docker 镜像名称 (用于 M6 初始状态验证和 M7 回归验证)",
    )
    parser.add_argument(
        "--report",
        default="",
        help="质检报告输出路径 (默认：<project_dir>/qc_report.json)",
    )
    parser.add_argument(
        "--log",
        default=log,
        help="日志文件输出路径 (默认：不保存日志文件，只输出到控制台)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="静默模式：不在控制台输出日志，只保存到文件",
    )

    args = parser.parse_args()

    # 配置日志
    global logger
    verbose = not args.quiet
    if args.log:
        log_path = Path(args.log)
    else:
        # 自动生成日志文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = Path(f"quality_check_{timestamp}.log")
    
    logger = setup_logger(log_file=str(log_path) if args.log or not args.quiet else None, verbose=verbose)
    
    logger.info("=" * 80)
    logger.info("User-Agentic 数据集质检脚本启动")
    logger.info(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"命令行参数：project_dir={args.project_dir or '(auto)'}, image={args.image or '(none)'}, report={args.report or '(default)'}")
    logger.info(f"日志文件：{log_path}")
    logger.info("=" * 80)

    if args.project_dir:
        target = Path(args.project_dir).resolve()
        if not target.is_dir():
            ERROR_MESSAGES.append(f"[目录扫描] 目录不存在：{target}")
            error_msg.append(f"错误：目录不存在：{target}")
            logger.error(f"错误：目录不存在：{target}")
            print(f"错误：目录不存在：{target}")
            sys.exit(1)
        project_dirs = [target]
        logger.info(f"指定项目目录：{target}")
    else:
        cwd = Path.cwd()
        if is_project_dir(cwd):
            project_dirs = [cwd]
            logger.info(f"当前目录是项目目录：{cwd}")
        else:
            project_dirs = find_project_dirs(cwd)
            if not project_dirs:
                ERROR_MESSAGES.append(f"[目录找到任何项目目录")
                error_msg.append(f"错误：当前目录下未找到项目目录 (需包含 trajectory.json)")
                logger.error(f"错误：当前目录下未找到项目目录 (需包含 trajectory.json)")
                error_msg.append(f"当前目录：{cwd}")
                logger.error(f"当前目录：{cwd}")
                logger.error(f"用法：python quality_check.py [project_dir] [--image IMAGE]")
                print(f"错误：当前目录下未找到项目目录 (需包含 trajectory.json)")
                print(f"当前目录：{cwd}")
                # print(f"用法：python quality_check.py [project_dir] [--image IMAGE]")
                sys.exit(1)
            logger.info(f"自动发现 {len(project_dirs)} 个项目目录")

    logger.info(f"\n开始检查 {len(project_dirs)} 个项目")
    
    all_passed = True
    for idx, project_dir in enumerate(project_dirs, 1):
        logger.info(f"\n{'=' * 80}")
        logger.info(f"进度：{idx}/{len(project_dirs)}")
        logger.info(f"{'=' * 80}")
        
        passed = run_checks(project_dir, args.image, args.report)
        overall_error_messages.extend(ERROR_MESSAGES)
        if not passed:
            all_passed = False
            logger.warning(f"项目 {project_dir.name} 检查失败")
        else:
            logger.info(f"项目 {project_dir.name} 检查通过")

    if len(project_dirs) > 1:
        logger.info(f"\n{'=' * 80}")
        overall = "PASS" if all_passed else "FAIL"
        logger.info(f"批量质检完成：{len(project_dirs)} 个项目，最终结果：{overall}")
        logger.info(f"{'=' * 80}")

    logger.info(f"\n质检完成！日志已保存到：{log_path}")
    # sys.exit(0 if all_passed else 1)
    return all_passed , overall_error_messages

if __name__ == "__main__":
    main()
