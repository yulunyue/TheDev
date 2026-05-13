## QtMessageItem

消息项组件，根据 status 显示不同颜色：

| status | title | 颜色 |
|--------|-------|------|
| running | 执行中 | 蓝色 #3498db |
| completed | 执行完成 | 绿色 #27ae60 |
| failed | 执行失败 | 红色 #c0392b |
| blocked | 执行阻塞 | 橙色 #e67e22 |

属性：
- key: 消息的唯一标识
- data: 完整消息数据

数据格式：
```json
{
    "key": "abc123",
    "title": "执行中",
    "status": "running",
    "user": "zhangsan"
}
```

显示格式：`{user} - oc_{key} {title}`

## QtMessageList

消息列表组件：
- show_keys: 允许显示的 key 列表（从配置获取）
- all_messages: 存储所有消息数据（不丢失）
- displayed_items: 当前显示的消息组件

功能：
- 订阅 TOPIC_MSG_QT 接收消息
- 订阅 TOPIC_QT_CONFIG_UPDATE 接收配置更新
- 配置变更时保留消息数据，重新过滤显示
- 同一个 key 只显示一条消息，新状态更新现有消息（位置不变）
- 新消息插入顶部

配置文件：config/setting/qt_show.json
```json
{
    "show_keys": ["test001", "opencode_main"]
}
```