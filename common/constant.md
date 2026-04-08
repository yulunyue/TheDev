# Constant 模块文档

## 文件概述
`constant.py` 定义了项目中的常量和数学计算工具类，为整个项目提供统一的常量定义和基础数学运算功能。

## 主要类和功能

### Constant 类
**用途**: 存储应用程序级别的常量定义

**主要常量**:
- `APP_NAME = "TheDev"` - 应用程序名称
- `CODE_500 = 500` - HTTP 500错误码
- `CODE_200 = 200` - HTTP 200成功码
- `TYPE = "type"` - 类型字段名
- `KEY = "key"` - 键字段名
- `DATA = "data"` - 数据字段名
- `VALUE = "value"` - 值字段名
- `METHOD_INSERT_UPDATE = "INSERT_UPDATE"` - 插入更新方法名
- `THE_DEV_USER = "the_dev_user"` - 默认用户名
- `USERNAME = "username"` - 用户名字段名
- `PASSWORD = "password"` - 密码字段名
- `METHOD_LOGIN = "login"` - 登录方法名

### CT (Constant Tools) 类
**用途**: 提供数学计算相关的常量和工具函数

**常量**:
- `MOD = (10**9) + 7` - 模运算常量（常用于算法题）
- `MX = (10**5) + 1` - 数组大小上限
- `inf = float("inf")` - 无穷大

**工具函数**:
- `min(a, b)` - 返回两个数中的较小值
- `max(a, b)` - 返回两个数中的较大值

### 全局实例
- `C = THE_DEV_CONSTANT = Constant()` - 全局常量实例

## 使用示例

```python
from common.constant import C, CT

# 使用应用常量
app_name = C.APP_NAME  # "TheDev"
username = C.USERNAME  # "username"
success_code = C.CODE_200  # 200

# 使用数学工具
min_val = CT.min(5, 10)  # 5
max_val = CT.max(5, 10)  # 10
mod_val = CT.MOD  # 1000000007
```

## 测试文件
- `constant_test.py` - 包含常量模块的单元测试

## 依赖关系
无外部依赖

## 修改注意事项
1. 添加新常量时，建议按照功能分组
2. 数学工具函数保持简洁高效
3. 考虑向后兼容性，避免修改现有常量的值