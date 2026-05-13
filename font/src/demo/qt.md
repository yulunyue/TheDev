## Qt 页面

Qt 窗口主入口，组合 QtDragBar 和 QtMessageList。

### 文件结构

```
font/src/demo/
├── qt.ts              # 主入口，组合组件
├── qt_drag_bar.ts     # 拖动条组件
├── qt_message_list.ts # 消息列表组件
```

### QtMain

主组件：
- init_node(): 添加 QtDragBar 和 QtMessageList
- init_style(): 全屏 flex 布局
- init_event():
  - 订阅 TOPIC_QT_CONFIG_UPDATE 接收配置更新
  - 订阅 TOPIC_MSG_QT 接收消息
  - 初始化获取配置

### 消息格式

接收的 WebSocket 消息格式（Node value 结构）：
```json
{
    "key": "abc123",
    "title": "执行中",
    "status": "running",
    "user": "zhangsan"
}
```

显示格式：`{user} - oc_{key} {title}`

### 配置过滤

只显示配置文件 `config/setting/qt_show.json` 中 `show_keys` 包含的 key。

配置变更时：
- 保留现有消息数据
- 重新过滤显示