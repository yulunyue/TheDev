# YML 模块文档

## 文件概述
`yml.py` 提供了一个简单的 YAML 解析器，支持将 YAML 格式的字符串转换为字典结构，并提供便捷的数据访问接口。

## 主要功能

### 工具函数
- `value_parse(s: str)`: 解析 YAML 值字符串
  - 去除字符串两端的引号（单引号或双引号）
  - 返回解析后的值

### 常量
- `VALUE_KEY = "__VALUE"` - 用于存储值的键名

### Yml 类
**用途**: YAML 解析器和数据访问器

**属性**:
- `data`: 解析后的数据字典

**主要方法**:

**解析方法**:
- `str_to_dict(self, datas: str)`: 将 YAML 字符串转换为字典
  - 支持 2 空格缩进
  - 忽略空行和注释（以 # 开头）
  - 使用栈结构处理嵌套关系
  - 只创建不重复的键

**数据加载**:
- `load(self, s)`: 加载 YAML 字符串
  - 解析字符串并存储到 `self.data`
  - 返回 self 支持链式调用

**数据访问**:
- `get(self, keys, defalut_value=None)`: 获取嵌套数据
  - `keys`: 可以是字符串（用 "." 分隔）或列表
  - `defalut_value`: 默认值，键不存在时返回
  - 支持多层嵌套访问

## 使用示例

```python
from common.util.yml import Yml

# 基本 YAML 解析
yml_content = """
database:
  host: localhost
  port: 5432
  name: mydb

server:
  host: 0.0.0.0
  port: 8080
  debug: true

features:
  - feature1
  - feature2
  - feature3
"""

yml = Yml()
yml.load(yml_content)

# 访问数据
db_host = yml.get("database.host")  # "localhost"
db_port = yml.get("database.port")  # 5432
server_host = yml.get("server.host", "default")  # "0.0.0.0"
nonexistent = yml.get("nonexistent.key", "default")  # "default"

# 使用列表键访问
features = yml.get("features")  # ["feature1", "feature2", "feature3"]
first_feature = yml.get("features.0")  # "feature1"

# 链式调用
yml.load(new_yaml_content).get("some.key")
```

## YAML 语法支持

### 支持的特性
- **缩进**: 2 空格缩进表示层级关系
- **注释**: 以 # 开头的行会被忽略
- **键值对**: `key: value` 格式
- **字符串**: 支持单引号和双引号字符串
- **空值**: 空值会被解析为空字符串
- **嵌套结构**: 支持多层级嵌套

### 不支持的功能
- 列表内嵌套对象（只支持简单列表）
- 多行字符串
- 引用和锚点
- 复杂数据类型（日期、正则表达式等）

## 实现原理
1. **行解析**: 逐行解析 YAML 内容
2. **缩进检测**: 通过空格数量确定层级关系
3. **栈结构**: 使用栈维护当前嵌套层级
4. **键值分离**: 通过冒号分离键和值
5. **值解析**: 处理引号和类型转换

## 依赖关系
无外部依赖

## 测试文件
无对应的测试文件

## 修改注意事项
1. YAML 解析器功能相对简单，不支持完整 YAML 规范
2. 缩进必须使用 2 个空格，不支持制表符
3. 键名不能为空
4. 嵌套结构中的重复键会被后出现的覆盖
5. 字符串解析只支持单引号和双引号
6. 数字和布尔值会被解析为字符串
7. 对于复杂的 YAML 文件，建议使用专业的 YAML 库