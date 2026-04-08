# Logger 模块文档

## 文件概述
`logger.py` 提供了一个增强版的日志记录器 `Logger`，继承自 Python 标准库的 `logging.Logger`，添加了文件处理、缓存管理和自定义格式化等功能。

## 主要功能

### 常量定义
- `DEFAULT_FMT`: 默认日志格式，包含时间、文件路径、函数名和信息
- `DEBUG_FMT`: 调试模式格式，只显示消息内容

### Logger 类
**用途**: 增强版日志记录器，支持文件输出、缓存和特殊功能

**继承关系**:
- `logging.Logger` - Python 标准库日志记录器

**属性**:
- `cache_msgs: list` - 消息缓存列表
- `path: str` - 日志文件路径
- `fp: File` - 文件操作对象

**构造函数**:
- `__init__(self, name, fmt, mode="w")`: 初始化日志记录器
  - `name`: 日志器名称
  - `fmt`: 日志格式
  - `mode`: 文件打开模式，默认为 "w"

**主要方法**:

**错误捕获**:
- `run_capture_error(self, f, *args, captures="", **kw)`: 运行函数并捕获特定错误
  - `f`: 要执行的函数
  - `captures`: 期望的错误消息前缀
  - 捕获到特定错误时记录调试信息
  - 否则重新抛出异常

**处理器管理**:
- `add_file_hander(self, fmt, mode)`: 添加文件处理器
  - 创建文件处理器并添加到日志记录器
  - 支持环境变量控制文件模式
  - 使用 UTF-8 编码

**缓存管理**:
- `get_and_clear_cache(self)`: 获取并清空消息缓存
  - 返回缓存的消息字符串
  - 清空缓存列表

**格式化输出**:
- `map(self, indent=" ", **kw)`: 格式化输出键值对
  - `indent`: 缩进字符
  - `**kw`: 键值对参数
  - 使用 `dict_to_str` 格式化并记录信息

**标准方法增强**:
- `debug()`: 增强的调试日志方法
- `info()`: 增强的信息日志方法
- 都支持 `stacklevel` 参数调整调用栈显示

## 日志格式

### 默认格式
```
[2023-01-01 12:00:00][/path/to/file.py:10][function_name] message
```

### 调试格式
```
message
```

## 使用示例

```python
from common.util.log.logger import get_log

# 获取日志记录器
logger = get_log("test", mode="a")

# 基本日志记录
logger.info("Hello World")
logger.debug("Debug message")

# 格式化输出
logger.map(key1="value1", key2="value2", indent=" ")

# 错误捕获测试
def error_function():
    raise ValueError("测试错误")

logger.run_capture_error(error_function, captures="测试错误")

# 消息缓存
logger.info("缓存消息1")
logger.info("缓存消息2")
cached = logger.get_and_clear_cache()
print(cached)  # "缓存消息1\n缓存消息2"
```

## 文件管理
- **自动创建**: 日志目录不存在时自动创建
- **模式控制**: 通过环境变量 `LOGGER_MODE` 控制文件打开模式
- **编码统一**: 使用 UTF-8 编码确保字符兼容性
- **路径标准化**: 使用 `name_to_path` 函数标准化日志文件路径

## 依赖关系
- `logging, logging.handlers` - Python 标准库日志
- `.util.name_to_path, File, LOGGER_MODE, dict_to_str, LOG_MAP` - 日志工具
- `os` - 操作系统接口

## 测试文件
无对应的测试文件

## 修改注意事项
1. 日志文件默认创建在 `data/log/` 目录下
2. 文件模式可以通过环境变量 `LOGGER_MODE` 覆盖
3. 消息缓存是有限的，长时间运行需要注意清理
4. 错误捕获功能只处理特定前缀的错误
5. 日志格式可以通过参数自定义
6. 文件编码固定为 UTF-8，不支持修改