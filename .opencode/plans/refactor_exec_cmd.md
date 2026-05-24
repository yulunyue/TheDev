# Refactor `_exec_cmd` — 提取 `_stream_output`

## 现状

`_exec_cmd` 46 行，嵌套两层 try，做了 3 件事：写 stdin、读 stdout 流、解析退出码。

## 改动

### 新增 `_stream_output(proc, sentinel) -> int`

```python
def _stream_output(self, proc, sentinel):
    for line in proc.stdout:
        line = line.rstrip("\n\r")
        if line == sentinel:
            break
        if not self._send_output(C.MSG_EXEC_STDOUT, data=line + "\n"):
            self._kill_process(proc)
            self.logger.warning("connection lost during exec, killed process")
            raise ConnectionError("connection lost")

    exit_code_line = proc.stdout.readline().strip()
    if exit_code_line:
        try:
            return int(exit_code_line)
        except (ValueError, TypeError):
            return -1
    return proc.poll() if proc.poll() is not None else -1
```

### 精简 `_exec_cmd` → ~22 行

```python
def _exec_cmd(self, msg: Node):
    with self._exec_lock:
        proc = self._ensure_shell()
        timer = None
        try:
            sentinel = f"---CMD_DONE_{uuid.uuid4().hex}---"
            cmd_line = self._build_cmd_line(msg.data["command"], sentinel)
            proc.stdin.write(cmd_line)
            proc.stdin.flush()

            timer = Timer(
                msg.data.get("timeout", 30), self._kill_process, args=(proc,)
            )
            timer.start()

            exit_code = self._stream_output(proc, sentinel)
            self._send_output(C.MSG_EXEC_DONE, exit_code=exit_code)
        except Exception as e:
            self._kill_process(proc)
            self._send_output(C.MSG_EXEC_DONE, exit_code=-1, error=str(e))
            self.logger.error(f"exec_cmd error: {e}")
        finally:
            if timer:
                timer.cancel()
```

### 关键变化

| 项 | 说明 |
|----|------|
| `timer` 移动到 `try` 外定义 | 确保 `finally` 中可安全 cancel |
| 连接断开用 `raise ConnectionError` | 替代 `return`，统一走外层 `except` |
| `_exec_cmd` 不再直接读写 stdout | 全部委托给 `_stream_output` |

## 影响范围

仅 `tool/service/agent_runner.py`，替换 `_exec_cmd` + 新增 `_stream_output`。测试无需变动，全部保持 green。
