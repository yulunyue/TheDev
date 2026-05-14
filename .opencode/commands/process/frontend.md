---
description: 管理前端 webpack 开发服务（启停/构建/状态）
---

你正在执行 `/process/frontend` 命令。

## 参数

`$1` — 操作，可选。值为 `start` / `stop` / `restart` / `build` / `status`。**未提供时默认 `status`**。

## 进程管理

- PID 文件：`data/proc/frontend.pid`
- 日志文件：`data/tmp/frontend.log`
- 端口：**8080**
- 使用 `ProcessLock("frontend")` 管理进程（`from common.tool.export import ProcessLock`）

## 执行流程

### start

1. 运行 `lsof -i :8080` 检查端口是否已被占用
2. 实例化 `ProcessLock("frontend")`，调用 `is_running()` 检查旧进程
3. **如存在旧进程**：向用户展示旧 PID 并请求确认后执行 `kill_old()`
4. **根据当前系统选择启动命令**：
   - **Linux / macOS**：使用 `setsid`（`nohup` 对 npm 不可靠）
     ```
     setsid sh -c 'cd font && npm start > data/tmp/frontend.log 2>&1 &'
     ```
   - **Windows**：使用 `cmd /c`
     ```
     cmd /c "cd font && npm start > data/tmp/frontend.log 2>&1"
     ```
   - 先执行 `uname -s` 检测系统类型（含 `MINGW` / `MSYS` → Windows，`Darwin` → macOS，`Linux` → Linux）
5. 将新 PID 写入 `data/proc/frontend.pid`
6. 等待 5 秒后用 `lsof -i :8080` 确认端口已监听
7. 如端口未监听，输出 `data/tmp/frontend.log` 尾部 20 行帮助排查

### stop

1. 实例化 `ProcessLock("frontend")`
2. 读取 PID，检查进程是否运行
3. **向用户确认后**调用 `kill_old()`（使用 `kill -9`）
4. 清理 PID 文件
5. 用 `lsof -i :8080` 确认端口已释放

### restart

1. 先执行 **stop** 流程
2. 再执行 **start** 流程

### build

1. 执行生产构建：
   ```
   cd font && npm run build
   ```
2. 输出构建结果，确认 `font/dist/` 目录已生成

### status（默认）

1. 运行 `lsof -i :8080` 检查端口状态
2. 读取 `data/proc/frontend.pid` 检查 PID 文件
3. 输出：进程 PID、运行状态、端口监听状态、日志文件路径

## 遵循规则

- **杀死进程前必须向用户确认**，避免误杀其他进程
- `nohup` 对 npm 不可靠，Linux/macOS 必须使用 `setsid`
- 所有临时输出写入 `data/tmp/`，禁止使用 `/tmp/`
- 启动失败时输出日志尾部辅助排查
- 不要修改 `tool/start.py`
