# Io TempFile 模块文档

## 文件概述
`tempfile.py` 定义了一个临时文件处理类 `TempFile`，支持内存中的临时数据存储，提供字符串和二进制数据的处理功能。

## 主要功能

### TempFile 类
**用途**: 内存中的临时文件处理，支持字符串和二进制模式

**类常量**:
- `BIN_MODE = "b"` - 二进制模式
- `STR_MODE = "s"` - 字符串模式

**属性**:
- `data`: 存储的数据，根据模式为 `bytes` 或 `str` 类型
- `mode`: 当前模式（"b" 或 "s"）

**构造函数**:
- `__init__(self, mode="b")`: 初始化临时文件
  - `mode="b"`: 二进制模式，data 为 bytes 类型
  - `mode="s"`: 字符串模式，data 为 str 类型
  - 默认使用二进制模式

**主要方法**:
- `write(self, d: bytes)`: 写入数据
  - `d`: 要写入的数据（bytes 或 str）
  - 根据当前模式自动转换数据类型
  - 追加模式写入，不覆盖原有数据
  - 支持链式调用

## 数据类型处理

### 二进制模式 (mode="b")
- `data`: bytes 类型
- 写入字符串时自动编码为 UTF-8
- 写入 bytes 时直接追加
- 适合处理二进制数据（图片、音频等）

### 字符串模式 (mode="s")
- `data`: str 类型
- 写入 bytes 时自动解码为 UTF-8
- 写入字符串时直接追加
- 适合处理文本数据

## 使用示例

```python
from common.util.io.tempfile import TempFile

# 二进制模式（默认）
bin_file = TempFile()  # 或 TempFile("b")
bin_file.write(b"Hello ")
bin_file.write("World")  # 自动编码
print(bin_file.data)  # b'Hello World'

# 字符串模式
str_file = TempFile("s")
str_file.write("Hello ")
str_file.write(b"World")  # 自动解码
print(str_file.data)  # 'Hello World'

# 链式调用
result = TempFile("s").write("Hello ").write("World ").data
print(result)  # 'Hello World '
```

## 应用场景
- **数据缓冲**: 临时存储处理过程中的数据
- **格式转换**: 在不同数据格式之间转换
- **测试模拟**: 模拟文件操作而不实际访问文件系统
- **数据拼接**: 高效拼接字符串或二进制数据
- **网络传输**: 临时存储网络传输的数据

## 性能特点
- **内存操作**: 所有操作都在内存中完成，速度快
- **自动类型转换**: 根据模式自动处理数据类型转换
- **追加模式**: 数据追加写入，保留历史数据
- **无文件IO**: 不涉及实际的文件系统操作

## 依赖关系
无外部依赖

## 测试文件
无对应的测试文件

## 修改注意事项
1. 数据存储在内存中，程序退出后数据会丢失
2. 大量数据存储时需要注意内存使用
3. 类型转换时要注意字符编码问题
4. 二进制模式适合处理非文本数据
5. 字符串模式适合处理文本数据
6. 可以扩展添加读取、清空、大小查询等方法
7. 当前实现不支持随机访问，只支持追加写入