# Io TCP Server 模块文档

## 文件概述
`tcp_server.py` 定义了 TCP 服务器类 `TcpServer`，继承自 `Server` 类，提供基于 TCP 协议的网络服务器功能。

## 主要功能

### TcpServer 类
**用途**: TCP 服务器实现，处理客户端连接请求和数据通信

**继承关系**:
- `Server` - 服务器基类
- `Io` - IO 基类

**主要方法**:

**套接字创建**:
- `create_socket(self)`: 创建 TCP 服务器套接字
  - 创建 `socket.AF_INET` (IPv4) 和 `socket.SOCK_STREAM` (TCP) 套接字
  - 设置为阻塞模式 (`setblocking(True)`)

**事件循环**:
- `loop(self)`: 服务器主循环
  - 监听客户端连接 (`listen(2048)`)
  - 接受新连接 (`accept()`)
  - 为每个客户端创建 TCP 客户端对象
  - 设置客户端参数并启动

## 使用示例

```python
from common.util.io.tcp_server import TcpServer
from common.util.io.tcp_client import TcpClient

# 创建 TCP 服务器
server = TcpServer()

# 设置服务器参数
server.set_addr(
    src_ip="127.0.0.1",  # 服务器 IP
    src_port=8080       # 服务器端口
)

# 启动服务器
server.start()

# 服务器会在新线程中运行，监听客户端连接
# 当客户端连接时，会自动创建 TcpClient 对象
```

## 工作流程
1. **套接字创建**: 创建 IPv4 TCP 套接字并设置为阻塞模式
2. **套接字初始化**: 绑定到指定地址和端口
3. **开始监听**: 调用 `listen(2048)` 开始监听连接
4. **接受连接**: 在循环中接受客户端连接
5. **客户端处理**: 为每个客户端创建 `TcpClient` 对象
6. **参数设置**: 设置客户端的源地址、目标地址和套接字
7. **启动客户端**: 调用 `start()` 在新线程中启动客户端

## TCP 服务器特性
- **多客户端**: 支持多个客户端同时连接
- **阻塞模式**: 使用阻塞式套接字，简化编程
- **线程池**: 每个客户端在独立线程中处理
- **连接管理**: 自动管理客户端连接的生命周期

## 依赖关系
- `.server.Server, socket` - 服务器基类和套接字
- `.tcp_client.TcpClient` - TCP 客户端类

## 测试文件
无对应的测试文件

## 修改注意事项
1. TCP 服务器需要绑定到可用的 IP 地址和端口
2. 端口号 1024 以下需要管理员权限
3. 连接队列大小设置为 2048，可根据实际需求调整
4. 阻塞模式简化了编程，但可能影响并发性能
5. 可以重写 `loop()` 方法添加自定义的连接处理逻辑
6. 长时间运行的服务器需要考虑资源清理和优雅关闭
7. 异常处理需要由调用者负责