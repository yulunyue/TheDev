---
description: 管理后端 Tornado 服务（启停/状态）
---

你正在执行 `/process/backend` 命令。

## 参数

`$1` — 操作，可选。值为 `start` / `stop` / `restart` / `status`。**未提供时默认 `status`**。

## 进程管理

- PID 文件：`data/proc/backend.pid`
- 日志文件：`data/tmp/backend.log`
- 端口：**9999**
- 使用 `ProcessLock("backend")` 管理进程（`from common.tool.export import ProcessLock`）

## 执行流程

### start

1. 运行 `lsof -i :9999` 检查端口是否已被占用
2. 实例化 `ProcessLock("backend")`，调用 `is_running()` 检查旧进程
3. **如存在旧进程**：向用户展示旧 PID 并请求确认后执行 `kill_old()`
4. 启动服务：
   ```
   nohup python main.py dev > data/tmp/backend.log 2>&1 &
   ```
5. 将新 PID 写入 `data/proc/backend.pid`
6. 等待 3 秒后用 `lsof -i :9999` 确认端口已监听
7. 如端口未监听，输出 `data/tmp/backend.log` 尾部 20 行帮助排查

### stop

1. 实例化 `ProcessLock("backend")`
2. 读取 PID，检查进程是否运行
3. **向用户确认后**调用 `kill_old()`（使用 `kill -9`）
4. 清理 PID 文件
5. 用 `lsof -i :9999` 确认端口已释放

### restart

1. 先执行 **stop** 流程
2. 再执行 **start** 流程

### status（默认）

1. 运行 `lsof -i :9999` 检查端口状态
2. 读取 `data/proc/backend.pid` 检查 PID 文件
3. 输出：进程 PID、运行状态、端口监听状态、日志文件路径

## 遵循规则

- **杀死进程前必须向用户确认**，避免误杀其他进程
- 所有临时输出写入 `data/tmp/`，禁止使用 `/tmp/`
- 启动失败时输出日志尾部辅助排查
- 不要修改 `tool/start.py`
