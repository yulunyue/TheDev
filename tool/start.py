import sys
import time
from common.tool.export import ProcessLock
from common.util.export import logger


def start_backend():
    lock = ProcessLock("backend")
    lock.start_process(
        ["python", "main.py", "dev"],
        log_file="data/tmp/backend.log"
    )
    logger.info("后端已启动, 端口=9999")
    time.sleep(2)


def start_frontend():
    lock = ProcessLock("frontend")
    lock.start_process(
        ["cmd", "/c", "npm start"],
        cwd="font",
        log_file="data/tmp/frontend.log"
    )
    logger.info("前端已启动, 端口=8080")
    time.sleep(2)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target == "backend":
        start_backend()
    elif target == "frontend":
        start_frontend()
    elif target == "all":
        start_backend()
        start_frontend()
    else:
        logger.error(f"未知目标: {target}")
        logger.info("用法: python tool/start.py [backend|frontend|all]")
        sys.exit(1)


if __name__ == "__main__":
    main()