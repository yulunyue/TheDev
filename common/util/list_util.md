# ListUtil 模块文档

## 文件概述
`list_util.py` 提供了一个列表工具类 `ListUtil`，用于简化列表的常用操作，包括查找、过滤、最大值/最小值计算等功能。

## 主要功能

### ListUtil 类
**用途**: 简化列表操作的工具类，提供链式调用接口

**属性**:
- `array: list` - 要操作的列表数据

**主要方法**:
- `__init__(array: list)`: 初始化列表工具类
- `get_one(func, get_value=None)`: 根据条件获取列表中的一个元素
  - `func`: 比较函数，接受两个参数，返回布尔值
  - `get_value`: 可选值提取函数，默认为 lambda a: a
  - 返回: (index, value) 元组
- `max(fn=None)`: 获取列表中的最大值
  - `fn`: 可选的值提取函数
  - 返回: (index, value) 元组
- `min(fn=None)`: 获取列表中的最小值
  - `fn`: 可选的值提取函数
  - 返回: (index, value) 元组
- `filter(fn)`: 根据条件过滤列表
  - `fn`: 过滤函数，返回布尔值
  - 返回: 过滤后的新列表

## 使用示例

```python
from common.util.list_util import ListUtil

# 基本使用
data = [3, 1, 4, 1, 5, 9, 2, 6]
list_util = ListUtil(data)

# 获取最大值
max_idx, max_val = list_util.max()
print(f"最大值: {max_val}, 索引: {max_idx}")

# 获取最小值
min_idx, min_val = list_util.min()
print(f"最小值: {min_val}, 索引: {min_idx}")

# 使用自定义函数获取元素
idx, val = list_util.get_one(lambda a, b: a > b and a > 5)
print(f"大于5的第一个值: {val}, 索引: {idx}")

# 过滤列表
filtered = list_util.filter(lambda x: x > 3)
print(f"大于3的元素: {filtered}")

# 复杂对象列表
users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 20}
]

user_util = ListUtil(users)
oldest_idx, oldest_user = user_util.max(fn=lambda u: u["age"])
print(f"最年长的用户: {oldest_user}")

# 过滤成年用户
adult_users = user_util.filter(lambda u: u["age"] >= 18)
print(f"成年用户: {adult_users}")
```

## 实现原理
- `get_one()`: 遍历列表，使用比较函数找到符合条件的第一个元素
- `max()/min()`: 基于比较函数实现，支持自定义值提取
- `filter()`: 使用列表推导式实现高效过滤

## 依赖关系
无外部依赖

## 测试文件
无对应的测试文件

## 修改注意事项
1. 列表在操作过程中不会被修改，返回新列表或新值
2. 比较函数应该返回布尔值，表示两个值的关系
3. 值提取函数用于从复杂对象中提取比较值
4. 空列表调用 `max()/min()` 会抛出异常
5. 工具类设计为不可变，不会修改原列表