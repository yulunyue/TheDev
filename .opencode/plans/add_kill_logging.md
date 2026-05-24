# Agent kill 链路日志

## 改动文件

`tool/service/agent_runner.py`

## 新增日志点

| 方法 | 位置 | 日志 |
|------|------|------|
| `_on_message` | kill 分支 | `self.logger.info(f"received MSG_EXEC_KILL from server")` |
| `_kill_exec` | kill 前后 | `self.logger.info(f"killing process pid={proc.pid}, running={proc.poll() is None}")` + kill 后 `self.logger.info(f"process killed, return_code={proc.poll()}")` |
| `_stream_output` | 循环正常退出（未 break sentinel） | `self.logger.warning("stream ended without sentinel, process may have been killed externally")` |
| `_stream_output` | 连接断开 | 已有 |
| `_exec_cmd` | 外层 exception | 已有 `self.logger.error(f"exec_cmd error: {e}")` |

## 排查步骤

1. 执行 `sleep 60` 等` timeout 较大的命令
2. 前端点"终止"
3. 查看 `data/log/agent/{agent_id}/` 下的日志
4. 确认 `received MSG_EXEC_KILL` 存在 → 消息到了
5. 确认 `killing process` 存在 → kill 执行了
6. 确认 `process killed, return_code=...` → 杀成功了
7. 确认 `stream ended without sentinel` → `_exec_cmd` 感知到了异常结束
