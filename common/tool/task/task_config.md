## task_config.py 变动记录

### 2026-05-10 args 替换为 kw

- 移除 `args = StrModel()` 字段
- 新增 `kw = JsonDictModel().set_title("参数")` 字段
- 修复 `get_form_columns()`：`cls.args` → `cls.kw`
