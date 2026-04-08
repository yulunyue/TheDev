# FileProcessor (FP) 模块文档

## 文件概述
`fp.py` 提供了一个强大的文件操作类 `File`，支持文件和目录的创建、读取、写入、复制、移动、压缩等多种操作，以及配置文件处理和 Excel 文件读取功能。

## 主要功能

### File 类
**用途**: 统一的文件和目录操作接口，支持多种文件格式的处理

**属性**:
- `path`: 文件路径（标准化为 "/" 分隔符）
- `dirs`: 目录列表
- `name`: 文件名（不含扩展名）
- `file_name`: 完整文件名
- `type`: 文件扩展名
- `m_time`: 文件修改时间
- `data`: 文件数据缓存

**类变量**:
- `FILES: Dict[str, "File"]` - 文件实例缓存，支持单例模式

#### 核心方法

**实例化和管理**:
- `new(path)`: 获取或创建文件实例（使用缓存）
- `get_size()`: 获取文件大小
- `get_m_time()`: 获取文件修改时间
- `get_m_time_str()`: 获取格式化的修改时间字符串
- `parent()`: 获取父目录文件对象
- `child(*args)`: 获取子文件/目录对象
- `get_abs_path()`: 获取绝对路径

**文件操作**:
- `make_dir_if_not_exist(is_dir=False)`: 递归创建目录
- `write_file(data, encoding="utf-8")`: 写入文件
  - 自动转换为 JSON 格式（如果是 dict/list）
  - 支持 bytes 和 str 类型
- `write_if_not_exists(data="")`: 仅在文件不存在时写入
- `read_data()`: 读取二进制数据
- `read_line()`: 按行读取文本
- `read_file(encoding="utf-8")`: 读取文件内容
  - 自动识别 JSON、CFG、INI、TOML 格式
  - 返回相应格式的数据结构

**文件系统操作**:
- `copy_to(dst: "File", over_write=False)`: 复制文件/目录
- `move_to(dst)`: 移动文件/目录
- `exists()`: 检查文件/目录是否存在
- `remove()`: 删除文件/目录
- `rename(src, dst)`: 重命名文件

**目录操作**:
- `list_dir(depth=1, with_dir=False, mathchs=None, ignores=None)`: 列出目录内容
- `list_tree_file(with_dir=False)`: 递归列出所有文件
- `is_dir()`: 判断是否为目录
- `is_file()`: 判断是否为文件

**特殊文件处理**:
- `is_json_file()`: 判断是否为 JSON 文件
- `py_module_path()`: 获取 Python 模块路径
- `dump_excel()`: 读取 Excel 文件（需要 pandas）
- `get_relative_path(path)`: 获取相对路径
- `dump()`: 根据文件类型进行特殊处理

**压缩操作**:
- `zip(dst=None, targets=None, ignores=None)`: 压缩文件/目录
- `unzip(dst=None)`: 解压文件

**高级功能**:
- `replace(info: dict)`: 文件内容替换
- `get_writer(mode="wb")`: 获取文件写入器
- `get_bin_writer()`: 获取二进制写入器
- `get_config()`: 获取配置文件内容
- `get(*keys, default_value=None)`: 获取嵌套配置值
- `read_fast_file()`: 快速读取文件（带缓存）

## 使用示例

```python
from common.util.fp import File

# 基本文件操作
file = File("data/test.txt")
file.write_file("Hello World")
content = file.read_file()
print(content)

# 目录操作
dir_file = File("data")
files = dir_file.list_dir(depth=2, mathchs=["*.py"])

# JSON 文件处理
json_file = File("config.json")
data = json_file.read_file()  # 自动解析为 dict
json_file.write_file({"key": "value"})  # 自动序列化

# 配置文件操作
config_file = File("config.cfg")
config = config_file.get_config()
value = config_file.get("database", "host", default_value="localhost")

# 压缩操作
zip_file = File("data").zip("data.zip")
zip_file.unzip("unzip_data")

# Excel 文件处理
excel_file = File("data.xlsx")
excel_data = excel_file.dump_excel()
```

## 支持的文件格式
- **文本文件**: .txt, .py, .md, .json
- **配置文件**: .cfg, .ini, .toml
- **压缩文件**: .zip
- **Excel 文件**: .xls, .xlsx（需要 pandas）

## 依赖关系
- `os` - 操作系统接口
- `json` - JSON 数据处理
- `typing.List, Dict` - 类型提示
- `zipfile` - ZIP 文件处理
- `shutil` - 文件操作工具
- `io` - 输入输出操作
- `.tool.time_format, json_dumps` - 工具函数

## 测试文件
无对应的测试文件

## 修改注意事项
1. 文件路径统一使用 "/" 分隔符，自动处理 Windows 路径
2. 文件读取时会自动识别格式并返回相应的数据结构
3. 文件操作会自动创建必要的目录
4. 文件实例会被缓存，避免重复创建
5. 压缩操作支持文件过滤和忽略规则
6. Excel 依赖 pandas 库，使用前需要确保安装
7. 配置文件支持嵌套结构，可通过 get 方法获取深层配置