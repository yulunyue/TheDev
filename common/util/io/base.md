# Io Base 模块文档

## 文件概述
`base.py` 定义了 IO 操作的基类 `Io`，提供了网络通信的基础接口，包括地址配置、日志记录、套接字管理等通用功能。

## 主要功能

### Io 类
**用途**: IO 操作基类，为网络通信提供统一的接口

**属性**:
- `sock: socket.socket` - 套接字对象
- `childs: Dict[str, "Io"]` - 子 IO 对象字典
- `_logger: Logger = None` - 日志记录器

**主要方法**:

**地址配置**:
- `set_addr(src_ip=None, src_port=None, dst_ip=None, dst_port=None)`: 设置地址信息
  - `src_ip`: 源 IP 地址
  - `src_port`: 源端口
  - `dst_ip`: 目标 IP 地址
  - `dst_port`: 目标端口
  - 返回 self 支持链式调用

**日志管理**:
- `set_logger(t)`: 设置日志记录器
  - `t`: 日志记录器对象
  - 返回 self 支持链式调用

**套接字管理**:
- `set_sock(sock)`: 设置套接字对象
  - `sock`: 套接字对象
  - 返回 self 支持链式调用
- `create_socket()`: 创建套接字（抽象方法，子类实现）
- `init_socket()`: 初始化套接字（抽象方法，子类实现）
- `init_data()`: 初始化数据（抽象方法，子类实现）

**通信接口**:
- `loop()`: 事件循环（抽象方法，子类实现）
- `run()`: 运行 IO 操作（抽象方法，子类实现）
- `write(data)`: 写入数据
  - 自动序列化字典数据
  - 支持字符串和字节数据
  - 调用 `send()` 方法发送
- `send(data)`: 发送数据（抽象方法，子类实现）

**线程管理**:
- `start()`: 在新线程中启动 IO 操作
  - 使用守护线程
  - 目标函数为 `run()`

**日志属性**:
- `logger`: 日志记录器属性
  - 如果未设置，自动创建日志记录器
  - 日志文件路径: `data/io/{class_name}/{src_ip}_{src_port}.log`

**字符串表示**:
- `__repr__()`: 返回 IO 对象的字符串表示
  - 格式: `{class_name} src={src_ip}:{src_port} dst={dst_ip}:{dst_port}`

## 使用示例

```python
from common.util.io.base import Io
import socket

# 创建自定义 IO 类
class CustomIo(Io):
    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def init_socket(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.src_ip, self.src_port))
    
    def init_data(self):
        self.childs = {}
    
    def loop(self):
        # 实现事件循环
        pass
    
    def run(self):
        # 实现运行逻辑
        self.create_socket()
        self.init_socket()
        self.init_data()
        self.loop()

# 使用 IO 基类
io = CustomIo()
io.set_addr(
    src_ip="127.0.0.1",
    src_port=8080,
    dst_ip="127.0.0.1", 
    dst_port=8081
).set_logger("custom_io")

# 启动 IO 操作
io.start()
```

## 设计模式
- **模板方法模式**: 定义 IO 操作的骨架，子类实现具体步骤
- **建造者模式**: 通过链式调用构建 IO 对象
- **策略模式**: 不同的子类实现不同的 IO 策略

## 依赖关系
- `threading.Thread` - 线程管理
- `socket` - 套接字操作
- `..log.logger, Logger, get_log` - 日志记录
- `typing.Dict, List` - 类型提示
- `time` - 时间处理
- `..tool.json_dumps` - JSON 序列化

## 测试文件
无对应的测试文件

## 修改注意事项
1. 子类必须实现抽象方法：`create_socket()`, `init_socket()`, `init_data()`, `loop()`, `run()`, `send()`
2. 日志文件路径是自动生成的，确保 `data/io/` 目录存在
3. 套接字操作需要处理异常情况
4. 子 IO 对象管理需要考虑线程安全
5. 数据写入会自动处理序列化，支持字典类型
6. 链式调用设计要求所有设置方法返回 self