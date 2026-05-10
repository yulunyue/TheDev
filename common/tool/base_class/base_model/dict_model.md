## dict_model.py 变动记录

### 2026-05-10 新增 JsonDictModel

- 新增 `JsonDictModel` 类，继承自 `DictModel`
- `get_type()` 返回 `"json"`（而非 `"pre"`），前端渲染为可编辑的 JSON 输入框
