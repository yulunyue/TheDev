# Tool 模块文档

## 文件概述
`tool.py` 是一个工具函数集合，提供了时间处理、唯一ID生成、编码解码、字符串处理、命令解析、JSON处理等多种实用工具函数。

## 主要功能

### 时间处理
- `time_format(timestamp)`: 格式化时间戳
  - 输入: Unix 时间戳
  - 输出: "YYYY-MM-DD HH:MM:SS" 格式的字符串

### 唯一ID生成
- `uid(s)`: 生成唯一标识符
  - 使用全局计数器 UK_MAP
  - 格式: "{s}_{counter}"
  - 示例: `uid("test")` 返回 "test_0", "test_1", ...

### Base64 编码解码
- `is_base64_code(s: str)`: 检查字符串是否为有效的Base64编码
- `base64_decode(s: str)`: Base64解码
- `base64_encode(s: str)`: Base64编码
- `b64_code(s: str)`: 智能Base64编解码
  - 尝试解码，失败则编码

### 字符串处理
- `ii(s: str)`: 解析整数列表
  - 从字符串中提取所有整数
  - 支持空格和换行分隔
- `str_mid(s: str, size, fill="-")`: 居中截断字符串
  - 超过指定长度时截断
  - 不足时用指定字符填充

### 哈希和加密
- `hash_any_str(c)`: 生成任意对象的字符串哈希
  - 递归处理字典和列表
  - 生成唯一的字符串表示
- `md5(c: str)`: 计算MD5哈希值

### 命令和URL解析
- `cmd_parse(s: str)`: 解析命令行参数
  - 支持键值对格式: key=value
  - 返回: (args_list, kwargs_dict)
- `url_to_json(params)`: URL参数转JSON
- `url_parse(s: str)`: 解析URL
  - 返回: (base_url, args_list, kwargs_dict)

### JSON处理
- `dict_to_str(indent=" ", **kw)`: 字典转字符串
  - 支持缩进格式
  - 浮点数保留3位小数
- `json_dumps(oj, indent=None)`: 增强的JSON序列化
  - 支持自定义对象序列化
  - 自动处理 set、ValuesView 等特殊类型
  - 支持 BaseModel 和 to_json 方法
- `assert_dict(a, b)`: 断言字典相等

### 字典操作
- `merge_dict(src, dst)`: 合并字典
  - 递归合并嵌套字典
  - 返回合并后的字典和操作记录

### 异常处理
- `asset_exception(fun, *args, msg="", **kw)`: 断言抛出异常
  - 执行函数并捕获异常
  - 验证是否抛出预期的异常

### 全局变量
- `THE_DEV_LOGER_PREFIX = "THE_DEV_LOGER_PREFIX"`
- `SYS_ARGS, SYS_KW = cmd_parse(sys.argv[1:])`: 命令行参数解析

## 使用示例

```python
from common.util.tool import (
    time_format, uid, base64_encode, base64_decode,
    ii, cmd_parse, url_parse, json_dumps, md5
)

# 时间格式化
timestamp = time.time()
formatted = time_format(timestamp)
print(formatted)  # "2023-01-01 12:00:00"

# 唯一ID生成
id1 = uid("user")  # "user_0"
id2 = uid("user")  # "user_1"

# Base64编解码
encoded = base64_encode("hello")
decoded = base64_decode(encoded)
print(encoded, decoded)  # "aGVsbG8", "hello"

# 智能Base64
result = b64_code("aGVsbG8")  # "hello"
result = b64_code("hello")     # "aGVsbG8"

# 整数解析
numbers = ii("1 2 3\n4 5 6")
print(numbers)  # [1, 2, 3, 4, 5, 6]

# 命令解析
args, kwargs = cmd_parse("arg1 arg2 key1=value1 key2=value2")
print(args, kwargs)  # ['arg1', 'arg2'], {'key1': 'value1', 'key2': 'value2'}

# URL解析
base_url, args, kwargs = url_parse("http://example.com/path?arg1=value1&key1=value2")
print(base_url, args, kwargs)

# JSON序列化
data = {"key": "value", "set": {1, 2, 3}}
json_str = json_dumps(data, indent=2)
print(json_str)

# MD5哈希
hash_value = md5("hello world")
print(hash_value)  # "5d41402abc4b2a76b9719d911017c592"

# 字典合并
src = {"a": 1, "b": {"c": 2}}
dst = {"b": {"d": 3}, "e": 4}
merged, record = merge_dict(src, dst)
print(merged, record)

# 异常断言
def test_function():
    raise ValueError("测试异常")

asset_exception(test_function, msg="应该抛出异常")
```

## 依赖关系
- `os` - 操作系统接口
- `typing.List` - 类型提示
- `json` - JSON处理
- `collections.defaultdict` - 默认字典
- `sys` - 系统参数
- `re` - 正则表达式
- `hashlib` - 哈希算法
- `base64` - Base64编解码
- `time` - 时间处理
- `collections.abc.ValuesView` - 值视图
- `..tool.base_class.base_model.model` - 模型基类

## 测试文件
无对应的测试文件

## 修改注意事项
1. UK_MAP 是全局状态，多线程使用时需要注意同步
2. Base64 解码会抛出异常，调用时需要处理
3. JSON 序列化支持自定义对象，需要实现相应方法
4. 字典合并会修改源字典
5. 时间格式化使用本地时区
6. 整数解析会跳过无法解析的值