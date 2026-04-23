# User API

## Overview

用户管理API，继承自 `FormBase`，提供用户数据的增删改查功能。数据持久化存储在 `config/setting/user.json`。

## API Endpoints

路由: `/app/user` (配置于 `config/setting/dev.json`)

| Method | Description |
|--------|-------------|
| `get(key)` | 获取指定用户实例 |
| `web_submit(type, value)` | 创建/更新用户 |
| `web_search(key, name)` | 搜索用户列表 |
| `to_table_view()` | 返回用户表格视图 |
| `to_form_row_view()` | 返回表单行视图 |
| `to_form_column_view()` | 返回表单列视图 |

## Data Model (UserModel)

| Field | Type | Description |
|-------|------|-------------|
| `name` | SearchModel | 用户名，可搜索 |
| `title` | StrModel | 用户标题 |
| `visite_num` | NumberModel | 访问次数，默认值 0 |
| `password` | EncroyModel | 密码，加密存储 |
| `user_type` | SelectModel | 用户类型，可选值: 0, 1, 2 |

## Usage Examples

```python
from app.tool.user import User, UserModel

# 获取用户
user = User().get("a")
print(user.name.get_value())

# 查询所有用户
users = UserModel.all()

# 创建用户
UserModel.insert("new_user", name="new", password="xxx", title="New User").save()

# 搜索用户
results = UserModel.query("a")
```

## Data Storage

文件: `config/setting/user.json`

```json
{
    "a": {
        "name": "a",
        "password": "aaav",
        "title": "123",
        "visite_num": 0.0
    }
}
```

## Class Hierarchy

```
FormBase (ApiBase)
    └── User
        └── model: UserModel (FileConfig -> ConfigBase)
```

## Related Files

- `common/tool/front/form_base.py` - FormBase 基类
- `common/tool/base_class/storege/file_config.py` - FileConfig 文件存储基类
- `common/tool/base_class/baseconfig.py` - ConfigBase 配置基类
- `common/tool/base_class/base_model/` - 字段类型定义