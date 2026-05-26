
#!/usr/bin/env python3
import subprocess
import sys
import os
import json
from pathlib import Path
import xml.etree.ElementTree as ET

# --- 配置 ---
# 请在这里设置你的代码仓库的绝对路径
REPO_PATH = "/testbed/cli"
# 要进行测试的基础 commit 哈希
BASE_COMMIT = "492687b0dafb7bec0d6281d019bb5f4f60439346"
# 实例ID，用于结果文件的顶级键
INSTANCE_ID = 'httpie__cli-927'

test_file = ['tests/test_uploads.py']

# --- 路径配置 (自动计算) ---
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = Path(REPO_PATH)

class Colors:
    """用于在终端中彩色打印的辅助类。"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

# 初始化结果字典
results = {
    INSTANCE_ID: {
        "patch_is_None": False,
        "patch_exists": True,
        "patch_successfully_applied": False,
        "resolved": False,
        "tests_status": {
            "FAIL_TO_PASS": {"success": [], "failure": []},
            "PASS_TO_PASS": {"success": [], "failure": []},
            "FAIL_TO_FAIL": {"success": [], "failure": []},
            "PASS_TO_FAIL": {"success": [], "failure": []}
        }
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
        process = subprocess.run(command, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=str(cwd))
        return True, process.stdout, process.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except FileNotFoundError:
        return False, "", f"Command '{command[0]}' not found."

def reset_repo(commit_hash):
    """重置仓库到指定的 commit，并强制清理所有未跟踪的文件。"""
    print_header(f"RESETTING REPO TO COMMIT: {commit_hash[:7]}")
    success, _, stderr = run_command(["git", "reset", "--hard", commit_hash], cwd=REPO_DIR)
    if not success:
        print(f"{Colors.RED}❌ ERROR: 'git reset --hard' failed.{Colors.ENDC}\n{stderr}")
        return False
    success, _, stderr = run_command(["git", "clean", "-fdx"], cwd=REPO_DIR)
    if not success:
        print(f"{Colors.RED}❌ ERROR: 'git clean -fdx' failed.{Colors.ENDC}\n{stderr}")
        return False
    print(f"{Colors.GREEN}✅ Repo has been forcefully reset and cleaned.{Colors.ENDC}")
    return True

def apply_patch(patch_path):
    """直接应用一个补丁文件。"""
    if not patch_path.exists():
        print(f"{Colors.YELLOW}ℹ️ Patch file {patch_path.name} not found, skipping.{Colors.ENDC}")
        return True
    print(f"{Colors.YELLOW}  -> Applying patch: {patch_path.name}{Colors.ENDC}")
    success, _, stderr = run_command(["git", "apply", str(patch_path)], cwd=REPO_DIR)
    if not success:
        print(f"{Colors.RED}❌ ERROR: Applying patch {patch_path.name} failed.{Colors.ENDC}\n{stderr}")
        return False
    print(f"{Colors.GREEN}✅ Applied patch {patch_path.name} successfully.{Colors.ENDC}")
    return True
    
def parse_junit_xml_report(report_path: Path):
    """解析 JUnit XML 报告并返回一个包含测试结果的字典。"""
    if not report_path.is_file():
        print(f"{Colors.RED}  -> FAILED: Pytest did not generate a report file at {report_path}.{Colors.ENDC}")
        return None
        
    test_results = {}
    try:
        tree = ET.parse(report_path)
        root = tree.getroot()
        for testcase in root.iter("testcase"):
            file_class_name = testcase.get("classname", "")
            file_name = testcase.get("file", "")
            test_name = testcase.get("name", "")
            file_class_path = file_class_name.replace(".", "/") + ".py"
            
            if file_name == file_class_path:
                nodeid = f"{file_class_path}::{test_name}"
            else:
                file_path = file_name + "::" + file_class_name.rsplit(".", 1)[-1]
                nodeid = f"{file_path}::{test_name}"
            
            failure_node = testcase.find("failure")
            error_node = testcase.find("error")
            skipped_node = testcase.find("skipped")

            if failure_node is not None or error_node is not None:
                test_results[nodeid] = "failed"
            elif skipped_node is None:
                test_results[nodeid] = "passed"
    except ET.ParseError as e:
        print(f"{Colors.RED}  -> FAILED: Could not parse the JUnit XML report: {e}{Colors.ENDC}")
        return None
    finally:
        if report_path.exists():
            os.remove(report_path)

    return test_results

def run_all_tests_and_get_results():
    print_header("RUNNING ALL TESTS WITH PYTEST")
    report_path = REPO_DIR / "test_report.xml"
    pytest_command = [
        "pytest", *test_file,
        "--junitxml", str(report_path),
        "--tb=short", "-o", "junit_family=xunit1",
        "-q"
    ]
    print(pytest_command)
    success, stdout, stderr = run_command(pytest_command, cwd=REPO_DIR, check=False)
    
    if not success:
        print(f"{Colors.RED}❌ ERROR: Pytest execution failed.{Colors.ENDC}\n{stderr}")
        return None

    test_results = parse_junit_xml_report(report_path)
    if test_results is None:
        return None

    total_tests = len(test_results)
    failed_tests = sum(1 for result in test_results.values() if result == "failed")
    passed_tests = total_tests - failed_tests

    print(f"{Colors.GREEN}✅ Pytest completed: {passed_tests}/{total_tests} tests passed.{Colors.ENDC}")
    return test_results

def write_results_and_exit(success=True):
    """将最终结果写入json文件并退出程序。"""
    output_path = SCRIPT_DIR / "results.json"
    print_header("FINAL STEP: WRITING results.json")
    try:
        with open(output_path, "w") as f: json.dump(results, f, indent=4)
        print(f"{Colors.GREEN}✅ Successfully wrote results to {output_path}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR: Could not write to {output_path}: {e}{Colors.ENDC}")
    sys.exit(0 if success else 1)

def main():
    global results
    
    # --- 补丁前运行 ---
    if not reset_repo(BASE_COMMIT): write_results_and_exit(False)
    if not apply_patch(SCRIPT_DIR / "test.patch"): write_results_and_exit(False)
    
    print_header("STEP 1: PRE-PATCH - Running tests with only test patch")
    pre_patch_results = run_all_tests_and_get_results()
    if pre_patch_results is None: write_results_and_exit(False)

    # --- 补丁后运行 ---
    # if not reset_repo(BASE_COMMIT): write_results_and_exit(False)
    # if not apply_patch(SCRIPT_DIR / "test.patch"): write_results_and_exit(False)
    if not apply_patch(SCRIPT_DIR / "code.patch"): write_results_and_exit(False)
    results[INSTANCE_ID]["patch_successfully_applied"] = True

    print_header("STEP 2: POST-PATCH - Running tests with both patches")
    post_patch_results = run_all_tests_and_get_results()
    if post_patch_results is None: write_results_and_exit(False)

    # --- 结果分类 ---
    print_header("STEP 3: CATEGORIZING RESULTS")
    all_tests_run = set(pre_patch_results.keys()) | set(post_patch_results.keys())
    
    for test in sorted(list(all_tests_run)):
        pre_status = pre_patch_results.get(test, "passed")
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
        if result["success"]: print(f"{Colors.GREEN}  [{category}]: {len(result['success'])} tests{Colors.ENDC}")
        if result["failure"]: print(f"{Colors.RED}  [{category}]: {len(result['failure'])} tests{Colors.ENDC}")

    fail_to_fail = results[INSTANCE_ID]["tests_status"]["FAIL_TO_FAIL"]["failure"]
    pass_to_fail = results[INSTANCE_ID]["tests_status"]["PASS_TO_FAIL"]["failure"]
    fail_to_pass = results[INSTANCE_ID]["tests_status"]["FAIL_TO_PASS"]["success"]

    if fail_to_pass and not fail_to_fail and not pass_to_fail:
        results[INSTANCE_ID]["resolved"] = True
        print(f"\n{Colors.GREEN}🎉🎉🎉 VERIFICATION SUCCESSFUL! 🎉🎉🎉{Colors.ENDC}")
        write_results_and_exit(True)
    else:
        print(f"\n{Colors.RED}❌❌❌ VERIFICATION FAILED! ❌❌❌{Colors.ENDC}")
        if not fail_to_pass: print(f"{Colors.YELLOW}  - No tests were fixed.{Colors.ENDC}")
        if fail_to_fail: print(f"{Colors.YELLOW}  - {len(fail_to_fail)} test(s) continued to fail (first 5): {fail_to_fail[:5]}{Colors.ENDC}")
        if pass_to_fail: print(f"{Colors.YELLOW}  - {len(pass_to_fail)} regression(s) detected (first 5): {pass_to_fail[:5]}{Colors.ENDC}")
        write_results_and_exit(False)

if __name__ == "__main__":
    if not REPO_PATH or not REPO_DIR.is_dir() or not (REPO_DIR / '.git').is_dir():
        print(f"{Colors.RED}错误：配置的仓库路径无效！{Colors.ENDC}")
        print(f"{Colors.YELLOW}请修改脚本顶部的 `REPO_PATH` 变量。{Colors.ENDC}")
        print(f"{Colors.YELLOW}当前配置路径: '{REPO_PATH}'{Colors.ENDC}")
        sys.exit(1)
    
    main()
