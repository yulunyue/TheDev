## Manage

管理类，提供文件上传、解压、重启服务等功能。

### send_msg

透传消息到指定 topic（WebSocket 群发）

参数：
- topic: 目标 topic 名称
- value: 消息内容（任意结构）

返回：Node(value=value)

示例：
```bash
curl -X POST "http://localhost:9999/app/manage/send_msg" \
  -H "Content-Type: application/json" \
  -d '{"topic":"TOPIC_MSG_QT","value":{"key":"abc123","title":"执行中","status":"running","user":"zhangsan"}}'
```

### get_qt_show_config

获取 Qt 显示配置

返回：Node(value={"show_keys": [...]})

示例：
```bash
curl -X POST "http://localhost:9999/app/manage/get_qt_show_config"
```

### update_qt_show_config

更新 Qt 显示配置并推送（读取 config/setting/qt_show.json 并推送到前端）

返回：Node(value={"show_keys": [...]})

示例：
```bash
curl -X POST "http://localhost:9999/app/manage/update_qt_show_config"
```