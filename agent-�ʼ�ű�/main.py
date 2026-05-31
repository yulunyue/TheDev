import json
from dockerbuild import build
from pathlib import Path
import quality_check
import db
from loguru import logger
import sys
import time
import zipfile
import shutil
# from delete_images import delete_docker

DELETE_IMAGE = True

# 读取配置文件（优先读取 exe 同目录下的 config.json）
config = {}
for cfg_candidate in [Path(sys.executable if getattr(sys, 'frozen', False) else __file__).parent / "config.json",
                       Path(__file__).parent / "config.json"]:
    if cfg_candidate.is_file():
        with open(cfg_candidate, "r", encoding="utf-8") as f:
            config = json.load(f)
        break

DATA_PATH = config.get("data_path", "./data")
LOG_PATH = config.get("log_path", "./logs")

class Tee(object):
    def __init__(self, filename):
        self.file = open(filename, "a", encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, data):
        self.stdout.write(data)
        self.file.write(data)

    def flush(self):
        self.stdout.flush()
        self.file.flush()

if __name__ == "__main__":
    db.init_db()
    db._migrate_db()
     # 从配置文件读取数据目录
    work_dir = DATA_PATH
    work_path = Path(work_dir)
    
    if not work_path.exists():
        logger.error("工作目录 {} 不存在", work_dir)
        sys.exit(1)
    
    # 获取质检数据目录下的所有子目录或zip压缩包作为任务
    tasks = []
    for item in work_path.iterdir():
        if item.is_dir():
            tasks.append({
                "path": item,
                "name": item.name,
                "is_temp": False,
                "archive_path": None
            })
        elif item.is_file() and item.suffix.lower() == ".zip":
            tasks.append({
                "path": item,
                "name": item.stem,
                "is_temp": True,
                "archive_path": item
            })
    
    if not tasks:
        logger.info("质检数据目录下没有找到任务目录或zip压缩包，程序结束。")
        sys.exit(0)

    # 保存原始的标准输出
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # 按字母顺序处理任务名称
    tasks.sort(key=lambda x: x["name"])
    
    # 用于收集全局所有任务的质检简要结果
    qc_summary_results = []
    
    for task_info in tasks:
        task_name = task_info["name"]
        batch_num = 'test'
        temp_cleanup_dir = None
        
        # 处理压缩包动态解包
        if task_info["is_temp"]:
            temp_parent = Path(DATA_PATH) / f".temp_extracted_{task_name}"
            # 确保先前残留被清除
            if temp_parent.exists():
                try:
                    shutil.rmtree(temp_parent)
                except Exception:
                    pass
            temp_parent.mkdir(parents=True, exist_ok=True)
            print(f"\n📦 检测到任务压缩包: {task_info['archive_path'].name}，正在自动解压到临时目录...")
            try:
                with zipfile.ZipFile(task_info["archive_path"], 'r') as zip_ref:
                    zip_ref.extractall(temp_parent)
                task_dir = temp_parent
                temp_cleanup_dir = temp_parent
            except Exception as e:
                logger.error(f"解压压缩包 {task_info['archive_path'].name} 失败: {e}")
                db.save_result(task_name, False, f"解压压缩包失败: {e}", batch_num, "")
                qc_summary_results.append({"task": task_name, "status": "FAIL", "reason": f"解压压缩包失败: {e}"})
                if temp_parent.exists():
                    try:
                        shutil.rmtree(temp_parent)
                    except Exception:
                        pass
                continue
        else:
            task_dir = task_info["path"]

         # 如果子目录中不存在trajectory.json文件，则寻找子目录中是否还有子目录，如果有，则继续处理子目录
        if not (task_dir / "trajectory.json").exists():
            for sub_dir in task_dir.iterdir():
                if sub_dir.is_dir():
                    task_dir = sub_dir
                    if(task_dir / "trajectory.json").exists():
                        break
                    else:
                        for sub_sub_dir in sub_dir.iterdir():
                            if sub_sub_dir.is_dir():
                                task_dir = sub_sub_dir
                                if(task_dir / "trajectory.json").exists():
                                    break
                                else:
                                    print("未找到trajectory.json文件，请勿嵌套多个子目录")
                                    continue
                if not sub_dir.exists():
                    break
        
        prompt = db.extract_prompt_from_trajectory(task_dir)
        tee = None  # 用于存储当前的 Tee 对象
        try:

            # 终端日志输出文件
            out_data = Path(LOG_PATH) / str(batch_num) / task_name
            out_data.mkdir(parents=True, exist_ok=True)
            out_data_file = str(out_data).replace("\\", "/") + "/" + task_name
            # 质检日志输出文件
            qc_log_file = f"{out_data_file}_qc.log"
            
            # 重定向标准输出和错误输出到日志文件
            tee = Tee(f"{out_data_file}.log")
            sys.stdout = tee
            sys.stderr = sys.stdout
            logger.remove()
            logger.add(sys.stdout, colorize=True)

            # 记录脚本开始时间
            start_time = time.time()
            print("脚本开始时间:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            # ==================== 构建阶段 ====================
            print("\n\n\n-----开始进行构建阶段-----\n\n\n")
            
            # 如果任务目录不存在，则下载任务数据
            # if not task_dir.exists():
            #     logger.info("任务目录不存在，开始下载: {}", task_name)
            #     get_data(None, task_name)
            
            # 构建选项
            FORCE_REBUILD = False
            SKIP_EXISTING = False

            # 构建镜像
            result = build(task_dir, FORCE_REBUILD, SKIP_EXISTING)
            print(result)
            if result.get("success", 0) < 1:
                logger.error("镜像构建失败,无法进行后续验证: {}", task_name)
                db.save_result(task_name, False, "镜像构建失败", batch_num, prompt)
                qc_summary_results.append({"task": task_name, "status": "FAIL", "reason": "镜像构建失败"})
                continue

            logger.success("镜像构建成功: {}", task_name)

            # ==================== 验证阶段 ====================
            print("\n\n\n-----开始进行验证阶段-----\n\n\n")
            
            # 进行验证
            # verify_info = verify(task_dir)
            print(f"   -> 镜像名称: {result.get('image_name')}")
            print(f"   -> 镜像大小: {result}")
            is_passed, error_msg = quality_check.main(task_dir,result.get("image_name"),qc_log_file)
            if is_passed:
                logger.success("质检通过: {}", task_name)
                db.save_result(task_name, True, batch_num=batch_num, prompt=prompt)
                qc_summary_results.append({"task": task_name, "status": "PASS", "reason": "所有模块全部通过"})
            else:
                logger.error("质检未通过: {}", task_name)
                logger.error(f"错误信息: {error_msg}")
                reason = "; ".join(str(m) for m in error_msg) if error_msg else "质检未通过"
                db.save_result(task_name, False, reason, batch_num, prompt)
                qc_summary_results.append({"task": task_name, "status": "FAIL", "reason": reason})
            logger.info(f"日志文件保存在:{out_data_file}.log")
            logger.info(f"脚本结束时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
            logger.info(f"共用时:{time.time() - start_time} 秒")
            # if DELETE_IMAGE:
            #     delete_docker([result.get("image_name")])
        except Exception as e:
            logger.error(f"处理 {task_name} 时出错: {e}")
            db.save_result(task_name, False, f"脚本执行异常: {e}", batch_num, prompt)
            qc_summary_results.append({"task": task_name, "status": "FAIL", "reason": f"脚本执行异常: {e}"})
            continue
        finally:
            # 恢复标准输出并关闭文件
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            if tee is not None:
                tee.file.close()
            logger.remove()
            
            # 如果是临时解压出的目录，执行完即刻彻底清理
            if temp_cleanup_dir and temp_cleanup_dir.exists():
                print(f"🧹 正在清理临时解压出的质检子目录: {temp_cleanup_dir}")
                try:
                    shutil.rmtree(temp_cleanup_dir)
                except Exception as e:
                    print(f"清理临时目录 {temp_cleanup_dir} 失败: {e}")

    # ==================== 打印全局多任务质检总报告 ====================
    print("\n" + "=" * 100)
    print("                              📊 全局质检多任务汇总报告 📊")
    print("=" * 100)
    total_tasks = len(qc_summary_results)
    passed_tasks = sum(1 for r in qc_summary_results if r["status"] == "PASS")
    failed_tasks = total_tasks - passed_tasks
    
    print("  总任务数：{:<6} |  通过数：\033[92m{:<6}\033[0m |  失败数：\033[91m{:<6}\033[0m".format(total_tasks, passed_tasks, failed_tasks))
    print("-" * 100)
    print("  {:<45} | {:<8} | {}".format("任务目录名称", "质检状态", "详细错误/原因"))
    print("-" * 100)
    
    # 11个质检模块的映射与默认启用状态（与 quality_check.py 保持完全一致）
    modules_config = [
        ("M1", True), ("M2", True), ("M3", True), ("M4", False), ("M5", False),
        ("M6", True), ("M7", True), ("M8", True), ("M9", True), ("M10", True), ("M11", True)
    ]
    
    for res in qc_summary_results:
        status_str = "\033[92mPASS\033[0m" if res["status"] == "PASS" else "\033[91mFAIL\033[0m"
        print("  {:<45} | {:<8} | {}".format(res['task'], status_str, res['reason']))
        
        # 绘制该文件夹下 11 个模块各自的 PASS / FAIL / SKIP 状态面板
        panel_items = []
        for name, is_enabled in modules_config:
            if not is_enabled:
                panel_items.append("\033[90m{}:-\033[0m".format(name))  # 灰色表示已跳过/禁用
            else:
                if res["status"] == "PASS":
                    panel_items.append("\033[92m{}:✓\033[0m".format(name))  # 绿色表示通过
                else:
                    if "镜像构建失败" in res["reason"] or "脚本执行异常" in res["reason"]:
                        panel_items.append("\033[91m{}:✗\033[0m".format(name))  # 全盘红色失败
                    else:
                        # 扫描错误原因，若包含该模块前缀则为 ✗，否则为 ✓
                        if "{}-".format(name) in res["reason"] or "[{}".format(name) in res["reason"]:
                            panel_items.append("\033[91m{}:✗\033[0m".format(name))  # 红色表示失败
                        else:
                            panel_items.append("\033[92m{}:✓\033[0m".format(name))  # 绿色表示通过
                            
        print("  └─ 模块指标状态： " + " ".join("[{}]".format(item) for item in panel_items))
    print("=" * 100 + "\n")
