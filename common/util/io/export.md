# Io Export 模块文档

## 文件概述
`export.py` 是 IO 模块的统一导出文件，将常用的 IO 相关类集中导出，方便其他模块直接引用。

## 主要功能

### 导出的类

**网络通信类**:
- `TcpServer` - TCP 服务器类
- `TcpClient` - TCP 客户端类

**文件处理类**:
- `TempFile` - 临时文件处理类

## 使用示例

```python
# 直接从 export 模块导入所需的类
from common.util.io.export import TcpServer, TcpClient, TempFile

# 创建 TCP 服务器
server = TcpServer()
server.set_addr(src_ip="127.0.0.1", src_port=8080)

# 创建 TCP 客户端
client = TcpClient()
client.set_addr(
    src_ip="127.0.0.1",
    src_port=8081,
    dst_ip="127.0.0.1",
    dst_port=8080
)

# 使用临时文件
temp_file = TempFile(mode="s")
temp_file.write("Hello World")
content = temp_file.data
print(content)  # "Hello World"
```

## 模块结构
```
common/util/io/
├── base.py          # IO 基类
├── client.py        # 客户端基类
├── export.py        # 统一导出
├── manage.py        # IO 管理器
├── server.py        # 服务器基类
├── tcp_client.py    # TCP 客户端
├── tcp_server.py    # TCP 服务器
└── tempfile.py      # 临时文件
```

## 依赖关系
- `.tcp_server.TcpServer` - TCP 服务器实现
- `.tcp_client.TcpClient` - TCP 客户端实现
- `.tempfile.TempFile` - 临时文件实现

## 测试文件
无对应的测试文件

## 修改注意事项
1. 新增导出的类需要确保在相应模块中已定义
2. 导出顺序应该按照使用频率或逻辑关系排列
3. 修改导出类可能会影响其他模块的导入
4. 建议保持导出接口的稳定性，避免频繁变更