# Agent 远程执行系统

## 概述

基于 TCP 的远程命令执行 + 交互式 Shell 系统。Agent 节点通过 TCP 连接到主服务器，接收并执行命令，流式回传输出。

## 架构

```
[agent_runner.py] ---TCP:20001---> [AgentTcpServer]
                                         │
                                  Manage.handler_agent_msg()
                                         │
                                  IO_MANAGE.agents / agent_clients
                                         │
                                  HTTP API ← [浏览器/Web]
```

## 已完成 (Phase 1-3)

### Phase 1 — TCP 通信框架

| 文件 | 改动 |
|------|------|
| `common/util/io/tcp_server.py` | 加 `CLIENT_CLASS = TcpClient` 类变量，loop 中用 `self.CLIENT_CLASS()` |
| `common/util/io/agent_client.py` | **新** `AgentTcpClient(Client)` — 4字节长度前缀帧 + JSON解析 + 断线自动注销 |
| `common/util/io/agent_server.py` | **新** `AgentTcpServer(TcpServer)` — CLIENT_CLASS=AgentTcpClient，收到消息路由到 manage |
| `common/util/io/manage.py` | +`agents: dict` + `agent_clients: dict` + register/unregister/heartbeat/list_agents |
| `main.py` | +`IO_MANAGE.start_agent_server()` 启动 TCP 监听 (默认 :20001) |

**消息帧格式:**
```
[4字节 Big-Endian 长度][UTF-8 JSON 体]
```

**Agent → Server 消息:**
| type | 说明 |
|------|------|
| `register` | `{agent_id, platform, hostname}` → 返回 `register_ok` |
| `heartbeat` | `{agent_id}` |
| `unregister` | `{agent_id}` |
| `exec_stdout` | `{cmd_id, data}` — 执行输出的 stdout 行 |
| `exec_stderr` | `{cmd_id, data}` — 执行输出的 stderr 行 |
| `exec_done` | `{cmd_id, exit_code}` — 执行完成 |

**Server → Agent 消息:**
| type | 说明 |
|------|------|
| `register_ok` | 注册确认 |
| `exec` | `{cmd_id, command, timeout}` — 执行命令 |

### Phase 2 — 远程执行 + OsUtil 改造

| 文件 | 改动 |
|------|------|
| `common/tool/os_util.py` | +`popen()` 方法 — 返回 `subprocess.Popen(stdout=PIPE, stderr=PIPE)` |
| `common/util/io/agent_client.py` | +`message_handler` 回调，支持 standalone 模式 |
| `common/util/io/agent_server.py` | 精简为 15 行：只取 `client.agent_id`，路由全交 manage |
| `common/util/io/manage.py` | +`handler_agent_msg()` 统一路由 + `send_exec()` 发送执行指令 + `store_agent_output()` |
| `tool/func/agent_runner.py` | **新** 远程 agent 主程序 (独立进程) |

**agent_runner 启动方式:**
```bash
# Linux
python tool/func/agent_runner.py --server 1.14.97.154:20001 --id node-1

# Windows
python tool/func/agent_runner.py --server 1.14.97.154:20001 --id win-pc --platform windows
```

**agent_runner 功能:**
- TCP 连接服务器 → 注册 → 心跳 (每 15s) → 消息循环
- 收到 `exec` → `OsUtil.popen()` 执行 → 逐行回传 stdout
- 断线自动重连

### Phase 3 — HTTP API

| 文件 | 改动 |
|------|------|
| `app/tool/agent.py` | **新** `Agent(ApiBase)` — list/exec 端点 |
| `main.py` | +`/app/agent` 路由注册 |
| `AGENTS.md` | +前后端数据约定 (Node 返回格式) |
| `tests/app/tool/agent_test.py` | **新** API 测试 |

**API 端点:**
| 方法 | 路由 | 说明 |
|------|------|------|
| `list` | `POST /agent/list` | 返回所有 agent 状态 |
| `exec` | `POST /agent/exec` | 发送命令给指定 agent |

## 待完成 (Phase 4-5)

### Phase 4 — 交互式 Shell

- `common/util/io/agent_shell.py` — 交互式 Shell 封装
  - Linux: `pty.openpty()` + `subprocess.Popen` 创建伪终端
  - Windows: `subprocess.PIPE` + 线程读取
  - 支持 stdin 写入 + stdout/stderr 读取 + resize
- `common/util/io/agent_server.py` / `manage.py`:
  - Server → Agent: `shell_start` / `shell_stdin` / `shell_resize` / `shell_stop`
  - Agent → Server: `shell_stdout` / `shell_stderr` / `shell_end`
- 前端发送 `POST /agent/exec --shell true` 切换交互模式

### Phase 5 — Web 管理界面

- `font/src/demo/agent/agent_main.ts` — Agent 列表 + 控制面板
- `font/src/demo/agent/agent_terminal.ts` — 终端组件 (用 `<pre>` 或 xterm.js)
- 布局: 左列 agent 列表 (在线/离线状态) + 右列命令面板 / 终端输出
- IO_MANAGE 实时推送 agent 事件到前端

## 数据流示例

```
[agent_runner]                    [Server]                    [HTTP API]
     │                               │                           │
     │── register ──────────────→ handler_agent_msg              │
     │←── register_ok ──────────────│                           │
     │                               │                           │
     │                               │←── POST /agent/exec ── [客户端]
     │←── exec {cmd_id, command} ──── send_exec()               │
     │─→ exec_stdout {cmd_id, data} ─ store_agent_output()      │
     │─→ exec_stdout {cmd_id, data} ─ store_agent_output()      │
     │─→ exec_done {cmd_id, code} ── store_agent_output()       │
```

## 关键常量

- TCP 监听端口: `20001` (默认，在 `start_agent_server()` 可配置)
- 心跳间隔: 15s (agent_runner)
- 帧格式: 4 字节 Big-Endian 长度前缀 + JSON

## 测试

```bash
python -m pytest tests/common/util/io/ -v          # IO 层测试 (5个)
python -m pytest tests/app/tool/agent_test.py -v    # API 测试 (2个)
```

## 修改记录

### 2026-05-22
- 创建 `app/tool/agent.md` 文档
- Phase 1-3 完成

### Phase 1
- `tcp_server.py`: +CLIENT_CLASS 类变量
- `agent_client.py`: 帧收发 + JSON 解析 + message_handler
- `agent_server.py`: 消息路由到 manage
- `manage.py`: agents 字典 + register/heartbeat

### Phase 2
- `os_util.py`: +popen() 方法
- `agent_client.py`: +message_handler 回调
- `agent_server.py`: 精简为 transport 层
- `manage.py`: +handler_agent_msg + send_exec
- `agent_runner.py`: 远程 agent 主程序

### Phase 3
- `app/tool/agent.py`: HTTP API 端点
- `main.py`: 注册 /app/agent 路由
- `AGENTS.md`: 前后端数据约定
