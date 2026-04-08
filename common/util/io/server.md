# Io Server 模块文档

## 文件概述
`server.py` 定义了服务器基类 `Server` 和消息类 `SocketMsg`，提供网络服务器的基本功能，包括连接管理、消息接收和套接字初始化。

## 主要功能

### SocketMsg 类
**用途**: 封装 socket 消息信息

**属性**:
- `sender`: 消息发送者
- `recv`: 消息接收者
- `msg`: 消息内容

### Server 类
**用途**: 网络服务器基类，继承自 `Io`，提供服务器端的通用功能

**属性**:
- `msgs: List[SocketMsg]` - 消息列表，存储接收到的所有消息

**主要方法**:

**连接管理**:
- `new_connection(self, addr, t: "Client")`: 处理新连接
  - `addr`: 客户端地址
  - `t`: 客户端对象
  - 将客户端添加到子连接列表
  - 设置客户端的服务器引用
  - 同步日志记录器

**消息处理**:
- `receive_msg(self, client: "Io", msg)`: 接收客户端消息
  - `client`: 发送消息的客户端
  - `msg`: 消息内容
  - 将消息添加到消息队列

**运行控制**:
- `run(self)`: 服务器运行主流程
  - 创建套接字
  - 初始化套接字配置
  - 初始化数据结构
  - 启动事件循环
- `init_socket(self)`: 初始化服务器套接字
  - 设置套接字选项
  - 绑定到指定地址和端口
- `init_data(self)`: 初始化服务器数据
  - 创建子连接字典

## 使用示例

```python
from common.util.io.server import Server
from common.util.io.client import Client

# 创建服务器
server = Server()
server.set_addr(src_ip="127.0.0.1", src_port=8080)

# 创建客户端
client = Client()
client.set_addr(
    src_ip="127.0.0.1",
    src_port=8081,
    dst_ip="127.0.0.1", 
    dst_port=8080
)

# 启动服务器
server.start()

# 当客户端连接时，server.new_connection() 会被调用
# 当客户端发送消息时，server.receive_msg() 会被调用
```

## 工作流程
1. **套接字创建**: 调用 `create_socket()` 创建服务器套接字
2. **套接字初始化**: 设置套接字选项并绑定到指定地址
3. **数据初始化**: 创建子连接管理字典
4. **事件循环**: 启动 `loop()` 方法监听客户端连接
5. **连接处理**: `new_connection()` 方法处理新客户端连接
6. **消息接收**: `receive_msg()` 方法处理客户端消息

## 设计特点
- **异步处理**: 使用独立线程处理服务器运行
- **连接管理**: 维护客户端连接列表，支持多客户端
- **消息队列**: 存储接收到的消息，支持后续处理
- **日志记录**: 提供详细的连接和调试信息

## 依赖关系
- `typing.List` - 类型提示
- `.base.Io, socket` - IO 基类和套接字
- `.client.Client` - 客户端类

## 测试文件
无对应的测试文件

## 修改注意事项
1. 服务器需要正确设置源 IP 和端口
2. 子类需要实现 `create_socket()` 和 `loop()` 方法
3. 消息处理逻辑可以根据需求扩展
4. 套接字绑定地址需要确保端口未被占用
5. 客户端连接管理需要考虑并发安全性
6. 日志记录可以帮助调试服务器运行状态