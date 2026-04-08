# EnumUtil 模块文档

## 文件概述
`enum_util.py` 提供了枚举类型相关的工具类，支持自动枚举值生成和枚举值到字符串的转换功能，主要用于创建和管理枚举类型。

## 主要功能

### EnumCls 类
**用途**: 枚举类基类，提供枚举值到字符串的转换功能

**属性**:
- `_format`: 字典，存储枚举值到名称的映射

**主要方法**:
- `__init__()`: 初始化枚举类
  - 自动扫描类属性，构建值到名称的映射
  - 跳过以 "_" 开头的私有属性
  - 只处理 int 和 str 类型的枚举值
- `to_str(v)`: 将枚举值转换为对应的字符串
  - 如果值不存在于映射中，抛出异常
  - 返回枚举值的原始名称

### 全局变量
- `GLOBAL_ADD = 0` - 全局计数器，用于自动生成枚举值

### 工具函数
- `auto(v=None)`: 自动生成递增枚举值
  - `v=None`: 返回当前值并递增
  - `v=指定值`: 设置全局计数器为指定值，返回原值
  - 返回值: 当前使用的枚举值

## 使用示例

```python
from common.util.enum_util import EnumCls, auto

# 定义枚举类
class Status(EnumCls):
    ACTIVE = 1
    INACTIVE = 0
    PENDING = 2

# 使用枚举转换
status_str = Status().to_str(1)  # 返回 "ACTIVE"
print(status_str)

# 使用自动枚举生成
class Colors(EnumCls):
    RED = auto()      # 返回 0，GLOBAL_ADD 变为 1
    GREEN = auto()    # 返回 1，GLOBAL_ADD 变为 2  
    BLUE = auto()     # 返回 2，GLOBAL_ADD 变为 3

print(RED, GREEN, BLUE)  # 0, 1, 2

# 自定义起始值
auto(100)  # 设置 GLOBAL_ADD 为 100
value = auto()  # 返回 100，GLOBAL_ADD 变为 101
```

## 实现原理
1. **动态映射**: 在 `__init__` 中通过 `dir()` 获取所有属性
2. **类型过滤**: 只处理 int 和 str 类型的值
3. **反向映射**: 构建 `{value: name}` 的反向查找字典
4. **自动递增**: 使用全局变量管理枚举值的自动生成

## 依赖关系
无外部依赖

## 测试文件
无对应的测试文件

## 修改注意事项
1. 枚举类需要继承 `EnumCls` 才能自动构建映射
2. 私有属性（以 "_" 开头）会被自动跳过
3. 重复的枚举值会导致映射覆盖
4. `to_str()` 方法找不到对应值时会抛出异常
5. 全局计数器 `GLOBAL_ADD` 是全局状态，多线程使用时需要注意同步
6. 枚举值建议使用常量或自动生成，避免硬编码