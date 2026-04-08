# TheDevLogger 模块文档

## 文件概述
`the_dev_log.py` 提供了一个专门的项目日志记录器 `TheDevLoger`，支持文件写入、数据结构日志记录和可视化输出功能，专为 TheDev 项目设计。

## 主要功能

### TheDevLoger 类
**用途**: 项目专用日志记录器，支持多种数据类型的日志记录

**属性**:
- `name: str` - 日志记录器名称
- `_fp: File` - 文件操作对象（延迟初始化）

**主要方法**:

**文件操作**:
- `fp` (property): 获取文件操作对象
  - 延迟初始化，第一次访问时创建文件
  - 自动记录文件创建信息到主日志
- `get_writer()`: 获取文件写入器
  - 返回文件对象的写入器
- `write(self, msg)`: 写入消息
  - 自动处理字符串和字节数据类型
  - 统一使用 UTF-8 编码
  - 自动添加换行符
  - 立即刷新写入缓冲区

**日志方法**:
- `info(self, msg)`: 记录信息日志
  - 调用 `write()` 方法写入消息
- `debug(self, msg)`: 记录调试日志
  - 调用 `write()` 方法写入消息

**特殊日志功能**:
- `log_tree(self, g: List[List[int]], f=None, head=0)`: 记录树形结构
  - `g`: 树形结构的邻接表表示
  - `f`: 可选的节点处理函数
  - `head`: 根节点索引
  - 支持文本和图形两种输出方式
- `log_grid(self, n, m, f)`: 记录网格结构
  - `n`: 网格行数
  - `m`: 网格列数
  - `f`: 网格数据函数
- `map(self, indent=" ", **kw)`: 记录键值对
  - 使用 `dict_to_str` 格式化输出

## 使用示例

```python
from common.util.log.the_dev_log import get_dev_log

# 获取日志记录器
logger = get_dev_log("test")

# 基本日志记录
logger.info("Hello World")
logger.debug("Debug message")

# 文件写入
logger.write("直接写入文件")

# 键值对记录
logger.map(key1="value1", key2="value2", indent="  ")

# 树形结构记录
tree = [[1, 2], [2, 3], [3, 4]]  # 邻接表
logger.log_tree(tree, head=0)

# 网格结构记录
def grid_func(i, j):
    return i * j

logger.log_grid(3, 3, grid_func)
```

## 特殊功能

### 树形结构记录
支持两种输出方式：
1. **文本格式**: 使用 `StrUtil.format_g_tree` 生成文本树
2. **图形格式**: 使用 `PyGraphViz` 生成图形文件（PNG）

### 网格结构记录
将二维数据以网格形式输出，便于查看矩阵类数据。

### 文件管理
- **延迟创建**: 文件在第一次使用时创建
- **自动管理**: 文件路径自动标准化
- **编码统一**: 统一使用 UTF-8 编码

## 数据类型支持
- **字符串**: 直接记录
- **字节数据**: 自动解码为 UTF-8
- **其他类型**: 转换为字符串后记录
- **复杂数据**: 通过专用方法处理（树、网格等）

## 依赖关系
- `..fp.File` - 文件操作
- `.util.name_to_path, LOG_MAP, dict_to_str` - 日志工具
- `typing.List, Dict` - 类型提示
- `...tool.str_util.StrUtil` - 字符串工具
- `common.third_util.view.pygraphviz_util.PyGraphViz` - 图形可视化

## 测试文件
无对应的测试文件

## 修改注意事项
1. 文件在第一次访问时创建，确保目录存在
2. 写入操作会立即刷新，确保数据不丢失
3. 图形输出依赖 PyGraphViz 库，使用前需要安装
4. 树形和网格输出主要用于调试和数据可视化
5. 日志文件路径会根据名称自动生成
6. 异常处理功能被注释，如需使用可以取消注释
7. 建议使用 `get_dev_log()` 函数获取实例，而不是直接构造