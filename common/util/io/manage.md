# Io Manage 模块文档

## 文件概述
`manage.py` 提供了一个 IO 管理器 `Manage` 类，用于集中管理所有的 IO 连接，并提供消息处理功能。同时提供了一个全局的 `IO_MANAGE` 实例。

## 主要功能

### Manage 类
**用途**: IO 连接管理器，统一管理所有的 IO 对象

**属性**:
- `io_map: Dict[str, Io]` - IO 对象映射表，用户名到 IO 对象的映射

**主要方法**:
- `__init__()`: 初始化管理器
  - 创建空的 IO 映射表
- `handler_msg(self, io: Io, msg: Node)`: 处理消息
  - `io`: 发送消息的 IO 对象
  - `msg`: 消息内容（Node 类型）
  - 将 IO 对象按用户名存储到映射表中
  - 返回 self 支持链式调用

### 全局实例
- `IO_MANAGE = Manage()` - 全局 IO 管理器实例
  - 可在整个项目中直接使用
  - 避免重复创建管理器

## 使用示例

```python
from common.util.io.manage import IO_MANAGE
from common.util.io.base import Io
from common.util.node import Node

# 创建 IO 对象
io1 = Io()
io1.username = "user1"

io2 = Io() 
io2.username = "user2"

# 创建消息
msg = Node(type="message", value="Hello World")

# 通过全局管理器处理消息
IO_MANAGE.handler_msg(io1, msg)
IO_MANAGE.handler_msg(io2, msg)

# 访问管理的 IO 对象
user1_io = IO_MANAGE.io_map.get("user1")
user2_io = IO_MANAGE.io_map.get("user2")
```

## 管理功能
- **连接注册**: 通过用户名注册 IO 对象
- **消息路由**: 提供消息处理的统一接口
- **对象查找**: 通过用户名快速找到对应的 IO 对象
- **全局共享**: 单例模式确保全局只有一个管理器

## 依赖关系
- `.base.Io` - IO 基类
- `typing.Dict` - 类型提示
- `..node.Node` - 节点工具

## 测试文件
无对应的测试文件

## 修改注意事项
1. 用户名应该是唯一的，重复的用户名会覆盖之前的 IO 对象
2. 消息处理逻辑可以根据需求扩展
3. 全局管理器 `IO_MANAGE` 可以在任何地方直接使用
4. IO 对象需要设置 `username` 属性才能正确管理
5. 建议在连接建立时调用 `handler_msg` 方法进行注册
6. 可以扩展管理器添加连接状态监控、断线重连等功能