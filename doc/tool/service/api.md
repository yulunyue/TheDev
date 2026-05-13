```qt_status
qt_status {"key":"test001", "status":"running", "user":"opencode"}
```

发送 opencode session 状态消息到 Qt 窗口。

参数：
- key: session ID
- status: 状态英文 (running/completed/failed/blocked)
- user: 用户名

示例：
```bash
python tool/service/api.py qt_status abc123 running zhangsan
```