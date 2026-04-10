from ..os_util import OsUtil
from common.util.export import List, os, re, logger
import psutil


def print_process_info(proc):
    """打印单个进程的详细信息"""
    try:
        info = proc.info
        print(
            f"PID: {info['pid']:<6} | Name: {info['name']:<25} | "
            f"CPU%: {info['cpu_percent']:>5.1f} | "
            f"Memory(MB): {info['memory_info'].rss / 1024 / 1024:>7.2f} | "
            f"Status: {info['status']}"
        )
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass


def list_all_processes():
    """列出所有进程的详细信息"""
    # 一次性收集所有进程信息，避免多次调用导致进程状态改变
    procs = []
    for proc in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_info", "status"]
    ):
        procs.append(proc)
    # 第二次循环获取 CPU 使用率需要间隔 0.1 秒
    for proc in procs:
        try:
            proc.cpu_percent(interval=0.0)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    # 等待一小段时间让 CPU 使用率计算生效（可选）
    import time

    time.sleep(0.1)
    # 再次获取并打印
    for proc in procs:
        try:
            proc.cpu_percent(interval=0.0)  # 获取实际值
            info = proc.info
            print_process_info(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def kill_processes_by_name(name_pattern, confirm=True):
    """
    根据进程名称（支持部分匹配）批量终止进程
    :param name_pattern: 进程名包含的字符串（不区分大小写），例如 "chrome"
    :param confirm: 是否要求用户确认
    """
    killed = []
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if name_pattern.lower() in proc.info["name"].lower():
                if confirm:
                    print(
                        f"准备终止 PID: {proc.info['pid']}  Name: {proc.info['name']}"
                    )
                proc.kill()
                killed.append(proc.info["pid"])
                print(f"已终止 PID: {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            print(f"无法终止进程 {proc.info['pid']}: {e}")
    if not killed:
        print(f"未找到名称包含 '{name_pattern}' 的进程")
    else:
        print(f"共终止 {len(killed)} 个进程")


def kill_processes_by_pid_list(pid_list, confirm=True):
    """根据 PID 列表批量终止进程"""
    for pid in pid_list:
        try:
            proc = psutil.Process(pid)
            if confirm:
                print(f"准备终止 PID: {pid}  Name: {proc.name()}")
            proc.kill()
            print(f"已终止 PID: {pid}")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"无法终止 PID {pid}: {e}")


def main():
    print("===== 当前系统进程列表 =====")
    list_all_processes()
    print("\n请选择操作：")
    print("1. 按进程名模式批量终止（例如输入 'chrome' 将杀死所有包含 chrome 的进程）")
    print("2. 按 PID 列表批量终止（输入以逗号分隔的 PID，例如 1234,5678）")
    choice = input("请输入选项 (1/2): ").strip()
    if choice == "1":
        pattern = input("请输入进程名关键字（不区分大小写）: ").strip()
        if pattern:
            kill_processes_by_name(pattern)
        else:
            print("未输入有效关键字")
    elif choice == "2":
        pid_input = input("请输入要终止的 PID，多个用逗号分隔: ").strip()
        if pid_input:
            try:
                pids = [
                    int(x.strip()) for x in pid_input.split(",") if x.strip().isdigit()
                ]
                if pids:
                    kill_processes_by_pid_list(pids)
                else:
                    print("未输入有效的 PID")
            except ValueError:
                print("PID 格式错误")
        else:
            print("未输入 PID")
    else:
        print("无效选项")


def find_port(result: str, port):
    # 查找端口
    pattern = rf":{port}\s+"
    for line in result.split("\n"):
        if re.search(pattern, line):
            ret = line.strip().split(" ")
            return ret

    return [""]


class System:
    @classmethod
    def get_pid_by_port_windows(cls, port):
        statu, result, stderror = OsUtil("netstat").run("-ano")
        return find_port(result, port)[0]

    @classmethod
    def get_pid_by_port_linux(cls, port):
        statu, result, stderror = OsUtil("netstat").run("-nltp")
        pid = find_port(result, port)[-1]
        return pid.split("/")[0]

    @classmethod
    def get_pid_by_port(cls, port):
        if os.name == "nt":
            return cls.get_pid_by_port_windows(port)
        return cls.get_pid_by_port_linux(port)


if __name__ == "__main__":
    main()
