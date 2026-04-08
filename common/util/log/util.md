# LogUtil 模块文档

## 文件概述
`util.py` 提供了日志系统的工具函数和配置管理，包括日志路径生成、标准输出重定向和日志目录管理等功能。

## 主要功能

### 全局配置
- `LOG_PREFIX = ""` - 日志前缀
- `LOG_DIR = "data/log"` - 日志目录
- `JSON_TMP_FILE = File(f"{LOG_DIR}/tmp.json")` - JSON 临时文件
- `LOG_MAP = dict()` - 日志记录器映射表
- `LOGGER_MODE = "LOGGER_MODE"` - 日志模式环境变量名

### 动态目录配置
如果命令行参数中包含 `THE_DEV_LOGER_PREFIX`，日志目录会动态扩展：
```python
if THE_DEV_LOGER_PREFIX in SYS_KW:
    LOG_DIR += f"/{SYS_KW.pop(THE_DEV_LOGER_PREFIX)}"
```

### 工具函数

**路径管理**:
- `LOGER_PREFIX(name)`: 生成日志前缀参数
  - 返回: `f"{THE_DEV_LOGER_PREFIX}={name}"`
- `name_to_path(name: str)`: 将日志名称转换为文件路径
  - 替换 ":" 为 "_" 避免 Windows 文件名问题
  - 如果不包含 "/"，添加到默认日志目录
  - 确保文件路径以 ".log" 结尾

**标准输出重定向**:
- `std_mock(with_trace=True)`: 重定向标准输出到日志
  - `with_trace=True`: 包含调用栈信息
  - `with_trace=False`: 不包含调用栈信息

**重定向功能**:
- 拦截 `sys.stdout` 和 `sys.stderr` 的输出
- 将输出重定向到日志文件
- 支持调用栈跟踪
- 自动处理换行符

## 使用示例

```python
from common.util.log.util import std_mock, name_to_path, LOGER_PREFIX

# 生成日志前缀参数
prefix_param = LOGER_PREFIX("my_app")
print(prefix_param)  # "THE_DEV_LOGER_PREFIX=my_app"

# 转换日志名称到文件路径
log_path = name_to_path("test")
print(log_path)  # "data/log/test.log"

# 重定向标准输出到日志
with std_mock(with_trace=True):
    print("这条消息会记录到日志中")
    print("包含调用栈信息")

# 使用命令行参数动态设置日志目录
# python script.py THE_DEV_LOGER_PREFIX=my_app
# 日志目录会变成: data/log/my_app
```

## 标准输出重定向机制

### Tmp 类
- `data = ""` - 缓冲区
- `write(self, data: str)`: 写入方法
  - 缓冲数据直到遇到换行符
  - 可选择包含调用栈信息
  - 自动清空缓冲区
- `flush(self)`: 刷新方法
  - 调用原始错误流的刷新方法

### 重定向流程
1. 保存原始标准输出和错误流
2. 创建临时日志记录器
3. 创建 Tmp 类替换标准输出
4. 拦截所有输出并记录到日志
5. 支持调用栈跟踪（可选）

## 应用场景
- **调试输出**: 将 print 语句输出重定向到日志文件
- **错误追踪**: 记录标准错误输出
- **日志分类**: 通过前缀区分不同模块的日志
- **开发调试**: 在开发过程中临时启用输出重定向

## 依赖关系
- `..fp.File` - 文件操作
- `..tool.SYS_ARGS, SYS_KW, json_dumps, THE_DEV_LOGER_PREFIX, dict_to_str` - 工具函数
- `sys` - 系统接口
- `traceback` - 调用栈跟踪

## 测试文件
无对应的测试文件

## 修改注意事项
1. 日志目录默认为 `data/log/`，确保目录存在
2. 文件名中的冒号会被替换为下划线
3. 标准输出重定向是全局性的，会影响整个程序
4. 调用栈跟踪可能影响性能，生产环境建议关闭
5. 重定向后原始标准输出可以通过 `old_std` 访问
6. 临时文件 `JSON_TMP_FILE` 可以用于跨进程数据交换
7. 日志模式可以通过环境变量 `LOGGER_MODE` 控制