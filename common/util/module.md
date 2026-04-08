# Module 模块文档

## 文件概述
`module.py` 提供了模块动态加载和函数信息分析的功能，支持运行时模块导入、函数参数解析、异常捕获和模块管理等高级功能。

## 主要功能

### FunInfo 类
**用途**: 存储函数的详细信息，包括参数、文档、类型等

**属性**:
- `name`: 函数名
- `doc`: 函数文档字符串
- `args`: 位置参数列表
- `kw`: 关键字参数字典
- `has_args`: 是否有可变位置参数 (*args)
- `has_kw`: 是否有可变关键字参数 (**kwargs)
- `has_self`: 是否有 self 参数

**方法**:
- `load(name, doc, args, kw, has_args, has_kw, has_self)`: 加载函数信息
- `to_json()`: 转换为 JSON 格式，前端友好

### 工具函数

**函数分析**:
- `check_func_arg_kw(v)`: 检查函数参数类型
  - 返回: (positional_or_keyword_count, positional_only_count, keyword_only_count, has_args, has_kw)
- `get_function_info(v)`: 获取函数的完整信息
  - 解析函数签名、参数类型、默认值
  - 支持 type_info 注解
  - 返回 FunInfo 对象

**函数调用**:
- `call_func_auto(func, *args, **kw)`: 自动适配函数调用
  - 根据函数参数信息自动选择调用方式
  - 支持 *args 和 **kwargs 的自动适配

**模块操作**:
- `get_file_path_by_cls(cls)`: 获取类的源文件路径
- `run_catch_error(f, limit=0, **kw)`: 捕获并记录函数执行错误
  - 支持调用栈回溯
  - 可配置回溯深度
  - 返回详细的错误信息

### Module 类
**用途**: 模块动态加载和管理

**属性**:
- `use_cache`: 是否使用模块缓存

**方法**:
- `load_module(module_name, path=None)`: 动态加载模块
  - 支持临时添加路径
  - 可选择是否缓存
  - 自动清理模块缓存
- `load_module_object(src: str, path: str = None)`: 加载模块对象
  - 支持 `module::class` 和 `module::class::method` 格式
  - 自动处理路径和模块名转换

## 使用示例

```python
from common.util.module import Module, get_function_info, run_catch_error

# 动态加载模块
module_loader = Module(use_cache=False)
math_module = module_loader.load_module("math")
print(math_module.sqrt(4))  # 2.0

# 加载模块对象
obj = module_loader.load_module_object("os::path::join")
result = obj("folder", "file.txt")  # "folder/file.txt"

# 获取函数信息
import math
func_info = get_function_info(math.sqrt)
print(f"函数名: {func_info.name}")
print(f"参数: {func_info.args}")
print(f"文档: {func_info.doc}")

# 自动函数调用
def example_func(a, b, c=10, *args, **kwargs):
    return a + b + c + sum(args)

result = call_func_auto(example_func, 1, 2, 20, 3, 4, extra="test")
print(result)  # 1+2+20+3+4 = 30

# 异常捕获和记录
def error_function():
    raise ValueError("测试错误")

error_info = run_catch_error(error_function, limit=2)
print(error_info)  # 包含调用栈和局部变量的错误信息
```

## 实现原理
1. **函数分析**: 使用 `inspect` 模块解析函数签名和参数
2. **动态加载**: 使用 `importlib` 动态导入模块
3. **异常捕获**: 通过 `inspect.currentframe()` 获取调用栈信息
4. **类型注解**: 支持自定义 `type_info` 属性和标准类型注解

## 依赖关系
- `sys` - 系统相关功能
- `os` - 操作系统接口
- `inspect` - 检查对象
- `importlib` - 动态导入
- `common.util.fp.File` - 文件操作
- `common.tool.str_util.StrUtil` - 字符串工具
- `common.util.log.logger` - 日志记录

## 测试文件
无对应的测试文件

## 修改注意事项
1. 动态加载模块时注意路径管理和内存泄漏
2. 函数参数解析支持复杂的参数类型和注解
3. 异常捕获会返回详细的调用栈信息，可能包含敏感数据
4. 模块缓存会影响内存使用，根据需要选择是否启用
5. 自定义类型注解需要实现 `type_info` 属性
6. 函数调用适配器不支持所有可能的参数组合