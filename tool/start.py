import os
import sys
import time
import subprocess


class ProcessLock:
    def __init__(self, lock_file):
        self.lock_file = lock_file
        
    def acquire(self):
        try:
            os.makedirs(os.path.dirname(self.lock_file), exist_ok=True)
            return True
        except:
            return False
    
    def release(self):
        pass
    
    def get_pid(self):
        try:
            if os.path.exists(self.lock_file):
                with open(self.lock_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        return int(content)
        except:
            pass
        return None
    
    def set_pid(self, pid):
        try:
            with open(self.lock_file, 'w') as f:
                f.write(str(pid))
        except:
            pass
    
    def clear(self):
        try:
            if os.path.exists(self.lock_file):
                os.remove(self.lock_file)
        except:
            pass


def kill_process(pid):
    try:
        os.kill(pid, 9)
        time.sleep(0.5)
        return True
    except ProcessLookupError:
        return True
    except:
        return False


def start_backend():
    lock = ProcessLock('data/proc/backend.lock')
    
    old_pid = lock.get_pid()
    if old_pid:
        logger.info(f"终止旧后端进程: PID={old_pid}")
        if kill_process(old_pid):
            lock.clear()
    
    logger.info("启动后端服务器...")
    proc = subprocess.Popen(
        ['python', 'main.py', 'dev'],
        stdout=open('data/tmp/backend.log', 'w'),
        stderr=subprocess.STDOUT,
        cwd=os.getcwd()
    )
    
    lock.set_pid(proc.pid)
    logger.info(f"后端已启动: PID={proc.pid}, 端口=9999")
    
    time.sleep(2)
    return True


def start_frontend():
    lock = ProcessLock('data/proc/frontend.lock')
    
    old_pid = lock.get_pid()
    if old_pid:
        logger.info(f"终止旧前端进程: PID={old_pid}")
        if kill_process(old_pid):
            lock.clear()
    
    logger.info("启动前端服务器...")
    
    font_dir = os.path.join(os.getcwd(), 'font')
    proc = subprocess.Popen(
        ['cmd', '/c', 'npm start'],
        stdout=open('data/tmp/frontend.log', 'w'),
        stderr=subprocess.STDOUT,
        cwd=font_dir,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    lock.set_pid(proc.pid)
    logger.info(f"前端已启动: PID={proc.pid}, 端口=8080")
    
    time.sleep(2)
    return True


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    if target == 'backend':
        start_backend()
    elif target == 'frontend':
        start_frontend()
    elif target == 'all':
        start_backend()
        start_frontend()
    else:
        logger.error(f"未知目标: {target}")
        logger.info("用法: python tool/start.py [backend|frontend|all]")
        sys.exit(1)


if __name__ == '__main__':
    from common.util.export import logger
    main()