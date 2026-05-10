## export.ts 变动记录

### 2026-05-10 注册 JsonInput 组件

- 导入 `JsonInput` 类
- 注册 `"json"` 类型到 `DivFactory`：`DivFactory.register("json", () => new JsonInput())`
