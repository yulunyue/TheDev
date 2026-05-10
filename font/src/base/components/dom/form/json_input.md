## json_input.ts 变动记录

### 2026-05-10 新建 JsonInput 组件

- 新增 `JsonInput` 类，继承 `Div`，基于 `<textarea>` 元素
- `set_value(value)`: 将对象序列化为 JSON 字符串写入 textarea
- `get_value()`: 从 textarea 读取并解析 JSON，返回对象
- 字体使用 monospace，便于编辑 JSON
