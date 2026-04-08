# Io TCP Client 模块文档

## 文件概述
`tcp_client.py` 定义了 TCP 客户端类 `TcpClient`，继承自 `Client` 类，提供基于 TCP 协议的网络客户端功能。

## 主要功能

### TcpClient 类
**用途**: TCP 客户端实现，处理 TCP 连接和数据发送

**继承关系**:
- `Client` - 客户端基类
- `Io` - IO 基类

**主要方法**:

**数据发送**:
- `send(self, data)`: 发送数据
  - `data`: 要发送的数据
  - 使用 `sendall()` 确保数据完整发送
  - 阻塞式发送，直到所有数据发送完成

**套接字创建**:
- `create_socket(self)`: 创建 TCP 套接字
  - 创建 `socket.AF_INET` (IPv4) 和 `socket.SOCK_STREAM` (TCP) 套接字
  - 设置为阻塞模式

## 使用示例

```python
from common.util.io.tcp_client import TcpClient

# 创建 TCP 客户端
client = TcpClient()

# 设置连接参数
client.set_addr(
    src_ip="127.0.0.1",      # 本地 IP
    src_port=8081,           # 本地端口
    dst_ip="127.0.0.1",      # 目标服务器 IP
    dst_port=8080            # 目标服务器端口
)

# 连接到服务器
client.connect()

# 发送数据
client.send(b"Hello Server")

# 关闭连接
client.close()
```

## 工作原理
1. **套接字创建**: 创建 IPv4 TCP 套接字
2. **连接建立**: 调用 `connect()` 方法连接到服务器
3. **数据发送**: 使用 `sendall()` 方法发送数据
4. **数据接收**: 在独立线程中运行，持续接收服务器数据
5. **连接管理**: 自动处理连接断开和资源清理

## TCP 特性
- **面向连接**: 需要先建立连接才能通信
- **可靠传输**: TCP 提供数据包排序、重传和流量控制
- **字节流**: 数据以字节流形式传输，无消息边界
- **阻塞模式**: 发送和接收操作会阻塞直到完成

## 依赖关系
- `.client.Client` - 客户端基类
- `.base.socket` - 套接字模块

## 测试文件
无对应的测试文件

## 修改注意事项
1. TCP 客户端需要正确设置源地址和目标地址
2. 连接前确保服务器正在运行
3. 大文件发送时可能需要分块处理
4. 长时间连接需要考虑心跳机制
5. 异常处理需要由调用者负责
6. 可以重写 `create_socket()` 方法添加自定义套接字配置