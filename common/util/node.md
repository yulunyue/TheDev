# Node 模块文档

## 文件概述
`node.py` 提供了一个通用的节点类 `Node` 和相关的工具函数，用于构建树形数据结构，支持节点的创建、管理和类型注解功能。

## 主要功能

### Node 类
**用途**: 通用的树形节点类，支持灵活的属性配置和子节点管理

**属性**:
- `type`: 节点类型
- `code`: 节点代码
- `key`: 节点键
- `title`: 节点标题
- `value`: 节点值
- `size`: 节点大小
- `data`: 节点附加数据字典
- `parent`: 父节点引用
- `childs: List[Node]`: 子节点列表

**构造函数**:
- `__init__(code=None, type="", key="", title="", size=None, value=None, data=None, childs=None)`
  - 支持灵活的参数配置
  - 自动处理子节点的初始化
  - 调用 `init()` 方法进行自定义初始化

**链式设置方法**:
- `set_value(v)`: 设置节点值，返回 self
- `set_type(tp)`: 设置节点类型，返回 self
- `set_key(key)`: 设置节点键，返回 self
- `set_title(title)`: 设置节点标题，返回 self
- `set_data(**kw)`: 设置节点数据，返回 self

**节点管理方法**:
- `add_child(**kw)`: 添加子节点
- `add_node(*args)`: 批量添加子节点
- `get_childs()`: 获取子节点列表
- `get_type()`: 获取节点类型
- `get_title()`: 获取节点标题
- `get_data()`: 获取节点数据

**序列化方法**:
- `to_json(**kw)`: 转换为 JSON 格式

### 工具函数

**类工厂函数**:
- `cls_util(tp, **kwargs)`: 创建带类型信息的类
  - 返回的类具有 `type_info` 属性
- `enum_cls(*enums) -> Type[Node]`: 创建枚举节点类
  - 自动设置类型为 "enum"
  - 子节点为枚举值列表
- `search_cls(url)`: 创建搜索节点类
  - 自动设置类型为 "search"
  - 包含 URL 属性

## 使用示例

```python
from common.util.node import Node, enum_cls, search_cls

# 基本节点创建
root = Node(
    type="folder",
    key="root",
    title="根目录",
    value="根节点"
)

# 添加子节点
child1 = root.add_child(
    type="file",
    key="file1",
    title="文件1",
    value="内容1"
)

child2 = root.add_child(
    type="file", 
    key="file2",
    title="文件2",
    value="内容2"
)

# 链式调用
root.set_data(created="2023-01-01", modified="2023-01-02")

# 批量添加子节点
root.add_node("value1", "value2", "value3")

# 枚举节点创建
Status = enum_cls("ACTIVE", "INACTIVE", "PENDING")
status_node = Status()
print(status_node.get_type())  # "enum"

# 搜索节点创建
SearchNode = search_cls("/api/search")
search_node = SearchNode()
print(search_node.get_type())  # "search"

# 序列化
json_data = root.to_json()
print(json_data)
```

## 数据结构
节点支持的数据结构：
- **基本类型**: str, int, float, bool
- **容器类型**: dict, list
- **复杂对象**: 通过 data 字段存储
- **子节点**: 通过 childs 列表管理

## 依赖关系
- `json` - JSON 序列化
- `typing.List, Type` - 类型提示
- `..constant.THE_DEV_CONSTANT, CT` - 常量定义
- `.tool.uid` - 唯一ID生成

## 测试文件
无对应的测试文件

## 修改注意事项
1. 节点设计为可变对象，支持链式调用
2. 子节点可以是字典或 Node 对象
3. `init()` 方法可以在子类中重写进行自定义初始化
4. 序列化时包含所有基本属性和子节点
5. 类型注解通过 cls_util 函数实现
6. 枚举和搜索节点是特殊的节点类型