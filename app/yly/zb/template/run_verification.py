#!/usr/bin/env python3
import subprocess
import sys
import os
import json
from pathlib import Path
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")


# --- 配置 ---
# 请在这里设置你的代码仓库的绝对路径
class CS:
    ERROR = "error"
    PASSED = "passed"
    SUCCESS = "success"
    FAILURE = "failure"
    FAILED = "failed"
    RUN = "run"
    SKIPPED = "skipped"
    CHECKED = "checked"
    CRASH = "crash"
    PASS_TO_PASS = "PASS_TO_PASS"
    PASS_TO_FAIL = "PASS_TO_FAIL"
    FAIL_TO_PASS = "FAIL_TO_PASS"
    NO_FAIL_TO_PASS = "NO_FAIL_TO_PASS"
    NO_PASS_TO_PASS = "NO_PASS_TO_PASS"
    FAIL_TO_FAIL = "FAIL_TO_FAIL"
    RESULT_JSON_FILE = "python_test_result.json"
    RUN_VERIFICATION_PY = "run_verification.py"
    CODE_PATCH = "code.patch"
    DOCKERFILE = "Dockerfile"
    SETUP_ENV_SH = "setup_env.sh"
    SETUP_REPO_SH = "setup_repo.sh"
    TEST_PATCH = "test.patch"
    ZB_TASK_FAIL = "ZB_TASK_FAIL"
    NOT_FIND_CASES = "NOT_FIND_CASES"
    NET_WORK_ERROR = "NET_WORK_ERROR"
    PY_DEFAULT = "3.9"
    TEST_DEPENDS_CODE = "TEST_DEPENDS_CODE"
    CHANGE_FILES_TOO_MAX = "CHANGE_FILES_TOO_MAX"
    HAS_HEX_FILES = "HAS_HEX_FILES"
    TEST_RESULT_NO_CHANGE = "TEST_RESULT_NO_CHANGE"
    PIP_INSTALL_EROOR = "PIP_INSTALL_EROOR"
    DOCKER_BUILD_FAILED = "DOCKER_BUILD_FAILED"
    ISSUE_0 = "ISSUE_0"
    TEST_NO_SUCCESS_BUT_SHOULD_BE_RIGHT = "TEST_NO_SUCCESS_BUT_SHOULD_BE_RIGHT"
    BASE_COMMIT_ID_ERROR_FOR_RUN_TEST = "BASE_COMMIT_ID_ERROR_FOR_RUN_TEST"


PY_BIN = "%{PY_BIN}"
INSTANCE_ID = "%{INSTANCE_ID}"
REPO_PATH = "%{REPO_PATH}"
PY_MAIN_CMD = os.environ.get("ZB_PY_MAIN_CMD", "%{PY_MAIN_CMD}")
RUN_TYPE = os.environ.get("ZB_PY_TEST_TYPE", "")
# 要进行测试的基础 commit 哈希
BASE_COMMIT = "%{BASE_COMMIT}"
# 实例ID，用于结果文件的顶级键
CODE_PATCH = "code.patch"
# --- 路径配置 (自动计算) ---
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = Path(REPO_PATH)


class Colors:
    """用于在终端中彩色打印的辅助类。"""

    GREEN = "GREEN"
    RED = "RED"
    YELLOW = "YELLOW"
    BLUE = "BLUE"
    ENDC = "ENDC"


# 初始化结果字典
results = {
    INSTANCE_ID: {
        "patch_is_None": False,
        "patch_exists": True,
        "patch_successfully_applied": False,
        "resolved": False,
        "content_category": "%{content_category}",
        "tests_status": {
            "FAIL_TO_PASS": {"success": [], "failure": []},
            "PASS_TO_PASS": {"success": [], "failure": []},
            "FAIL_TO_FAIL": {"success": [], "failure": []},
            "PASS_TO_FAIL": {"success": [], "failure": []},
        },
    }
}

# --- 辅助函数 ---


def print_header(message):
    """打印格式化的标题。"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}=== {message}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.ENDC}")


def run_command(command, cwd, check=True):
    """运行一个子进程命令并返回结果。"""
    try:
        process = subprocess.run(
            command, check=check, capture_output=True, text=True, cwd=str(cwd)
        )
        return True, process.stdout, process.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except FileNotFoundError:
        return False, "", f"Command '{command[0]}' not found."


def reset_repo(commit_hash):
    """重置仓库到指定的 commit，并强制清理所有未跟踪的文件。"""
    print_header(f"RESETTING REPO TO COMMIT: {commit_hash[:7]}")
    success, _, stderr = run_command(
        ["git", "reset", "--hard", commit_hash], cwd=REPO_DIR
    )
    if not success:
        print(
            f"{Colors.RED}❌ ERROR: 'git reset --hard' failed.{Colors.ENDC}\n{stderr}"
        )
        return False
    success, _, stderr = run_command(["git", "clean", "-fd"], cwd=REPO_DIR)
    if not success:
        print(f"{Colors.RED}❌ ERROR: 'git clean -fd' failed.{Colors.ENDC}\n{stderr}")
        return False
    print(f"{Colors.GREEN}✅ Repo has been forcefully reset and cleaned.{Colors.ENDC}")
    return True


def apply_patch(patch_path):
    """直接应用一个补丁文件。"""
    if not patch_path.exists():
        print(
            f"{Colors.YELLOW}ℹ️ Patch file {patch_path.name} not found, skipping.{Colors.ENDC}"
        )
        return True
    print(f"{Colors.YELLOW}  -> Applying patch: {patch_path.name}{Colors.ENDC}")
    success, _, stderr = run_command(["git", "apply", str(patch_path)], cwd=REPO_DIR)
    if not success:
        print(
            f"{Colors.RED}❌ ERROR: Applying patch {patch_path.name} failed.{Colors.ENDC}\n{stderr}"
        )
        return False
    print(
        f"{Colors.GREEN}✅ Applied patch {patch_path.name} successfully.{Colors.ENDC}"
    )
    return True


def get_result(result_file):
    result = dict()
    ct = dict()
    crash = dict()
    if not os.path.exists(result_file):
        # print(f"{__file__} FILE_NOT_EXIST {result_file}")
        return result, ct, dict()

    def add_crash(crash_msg, node_id):
        if not crash_msg:
            return
        if len(crash_msg) > 100:
            crash_msg = crash_msg[:50] + "...." + crash_msg[-50:]
        crash[crash_msg] = crash.get(crash_msg, "") + " " + node_id

    with open(result_file, "r") as f:
        data = json.loads(f.read())
        for item in data.get("tests", []):
            if not item["nodeid"]:
                continue
            result[item["nodeid"]] = item["outcome"]
            ct[item["outcome"]] = ct.get(item["outcome"], 0) + 1
            crash_msg = ""
            if CS.CRASH in item.get("setup", dict()):
                crash_msg += item["setup"][CS.CRASH]["message"]
            elif CS.CRASH in item.get("call", dict()):
                crash_msg += item["call"][CS.CRASH]["message"]
            add_crash(crash_msg, item["nodeid"])

        for item in data.get("collectors", []):
            if not item["nodeid"]:
                continue
            crash_msg = ""
            if "longrepr" in item:
                crash_msg += item["longrepr"]
            add_crash(crash_msg, item["nodeid"])
    # os.system(f"rm -rf {result_file}")
    return result, ct, crash


def run_before_py_test():
    pass


def run_py_test(name):
    run_before_py_test()
    result_file = f"{REPO_DIR}/{CS.RESULT_JSON_FILE}"
    py_test_args = ["pytest", "--json-report", f"--json-report-file={result_file}"]
    if RUN_TYPE:
        statu_code, msg, msg1 = 0, "", ""
        import pytest

        os.chdir(REPO_DIR)
        pytest.main(PY_MAIN_CMD.split(" "))
    else:
        args = py_test_args + PY_MAIN_CMD.split(" ")
        print(" ".join(args))
        statu_code, msg, msg1 = run_command(args, cwd=REPO_DIR)

    os.system(f"cp {result_file} {name}.json")
    result, ct, crash = get_result(result_file)
    return statu_code, msg, msg1, ct, result, crash


def run_all_tests_and_get_results(name):
    """使用 poetry run pytest 运行所有测试并从 JUnit XML 报告中解析结果。"""
    # TODO
    statu_code, msg, msg1, ct, result, args = run_py_test(name)
    with open(f"{name}.log", "w", encoding="utf-8") as f:
        f.write(f"stdout=>{msg}\nstderr=>{msg1}\nct=>{ct}\nresult=>{result}")
    print(f"\nstatu_code=>{statu_code}\n")
    return result, ct


def write_results_and_exit(success=True):
    """将最终结果写入json文件并退出程序。"""
    output_path = SCRIPT_DIR / "results.json"
    print_header("FINAL STEP: WRITING results.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(
            f"{Colors.GREEN}✅ Successfully wrote results to {output_path}{Colors.ENDC}"
        )
    except Exception as e:
        print(
            f"{Colors.RED}❌ ERROR: Could not write to {output_path}: {e}{Colors.ENDC}"
        )
    sys.exit(0 if success else 1)


def do_pre():
    return run_all_tests_and_get_results("pre")


def do_test():
    if not apply_patch(SCRIPT_DIR / "test.patch"):
        write_results_and_exit(False)
    print_header("STEP 1: PRE-PATCH - Running tests with only test patch")
    pre_patch_results, _ = run_all_tests_and_get_results("test")
    if not pre_patch_results:
        write_results_and_exit(False)
    return pre_patch_results


def do_code():
    if not apply_patch(SCRIPT_DIR / "test.patch"):
        write_results_and_exit(False)
    elif not apply_patch(SCRIPT_DIR / CODE_PATCH):
        write_results_and_exit(False)
    results[INSTANCE_ID]["patch_successfully_applied"] = True

    print_header("STEP 2: POST-PATCH - Running tests with both patches")
    post_patch_results, _ = run_all_tests_and_get_results("code")
    if not post_patch_results:
        write_results_and_exit(False)
    return post_patch_results


def main():
    global results

    # (可选) 在开始前，可以运行一次 poetry install 确保环境是最新的
    print_header("Ensuring Poetry environment is up to date")
    # success, _, stderr = run_command(["poetry", "install"], cwd=REPO_DIR)
    # if not success:
    #     print(f"{Colors.RED}❌ ERROR: 'poetry install' failed.{Colors.ENDC}\n{stderr}")
    #     write_results_and_exit(False)

    # --- 补丁前运行 ---
    if not reset_repo(BASE_COMMIT):
        write_results_and_exit(False)
    pre_result, pre_ct = do_pre()
    if pre_ct.get(CS.FAILED) or pre_ct.get(CS.ERROR):
        write_results_and_exit(False)
    pre_patch_results = do_test()
    # --- 补丁后运行 ---
    if not reset_repo(BASE_COMMIT):
        write_results_and_exit(False)
    post_patch_results = do_code()
    # --- 结果分类 ---
    print_header("STEP 3: CATEGORIZING RESULTS")
    all_tests_run = set(pre_patch_results.keys()) | set(post_patch_results.keys())

    for test in sorted(list(all_tests_run)):
        pre_status = pre_patch_results.get(test, "failed")
        post_status = post_patch_results.get(test, "failed")

        if pre_status == "failed" and post_status == "passed":
            results[INSTANCE_ID]["tests_status"]["FAIL_TO_PASS"]["success"].append(test)
        elif pre_status == "passed" and post_status == "passed":
            results[INSTANCE_ID]["tests_status"]["PASS_TO_PASS"]["success"].append(test)
        elif pre_status == "failed" and post_status == "failed":
            results[INSTANCE_ID]["tests_status"]["FAIL_TO_FAIL"]["failure"].append(test)
        elif pre_status == "passed" and post_status == "failed":
            results[INSTANCE_ID]["tests_status"]["PASS_TO_FAIL"]["failure"].append(test)

    for category, result in results[INSTANCE_ID]["tests_status"].items():
        if result["success"]:
            print(
                f"{Colors.GREEN}  [{category}]: {len(result['success'])} tests{Colors.ENDC}"
            )
        if result["failure"]:
            print(
                f"{Colors.RED}  [{category}]: {len(result['failure'])} tests{Colors.ENDC}"
            )

    fail_to_fail = results[INSTANCE_ID]["tests_status"]["FAIL_TO_FAIL"]["failure"]
    pass_to_fail = results[INSTANCE_ID]["tests_status"]["PASS_TO_FAIL"]["failure"]
    fail_to_pass = results[INSTANCE_ID]["tests_status"]["FAIL_TO_PASS"]["success"]

    if fail_to_pass and not fail_to_fail and not pass_to_fail:
        results[INSTANCE_ID]["resolved"] = True
        print(f"\n{Colors.GREEN}🎉🎉🎉 VERIFICATION SUCCESSFUL! 🎉🎉🎉{Colors.ENDC}")
        write_results_and_exit(True)
    else:
        print(f"\n{Colors.RED}❌❌❌ VERIFICATION FAILED! ❌❌❌{Colors.ENDC}")
        if not fail_to_pass:
            print(f"{Colors.YELLOW}  - No tests were fixed.{Colors.ENDC}")
        if fail_to_fail:
            print(
                f"{Colors.YELLOW}  - {len(fail_to_fail)} test(s) continued to fail (first 5): {fail_to_fail[:5]}{Colors.ENDC}"
            )
        if pass_to_fail:
            print(
                f"{Colors.YELLOW}  - {len(pass_to_fail)} regression(s) detected (first 5): {pass_to_fail[:5]}{Colors.ENDC}"
            )
        write_results_and_exit(False)


if __name__ == "__main__":
    if not REPO_PATH or not REPO_DIR.is_dir() or not (REPO_DIR / ".git").is_dir():
        print(f"{Colors.RED}错误：配置的仓库路径无效！{Colors.ENDC}")
        print(f"{Colors.YELLOW}请修改脚本顶部的 `REPO_PATH` 变量。{Colors.ENDC}")
        print(f"{Colors.YELLOW}当前配置路径: '{REPO_PATH}'{Colors.ENDC}")
        sys.exit(1)
    if RUN_TYPE:
        run_all_tests_and_get_results(RUN_TYPE)
    else:
        main()
