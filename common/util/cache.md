# Cache 模块文档

## 文件概述
`cache.py` 提供了一个基于文件的缓存系统，支持数据持久化和全局缓存实例管理，主要用于将临时数据保存到文件系统中以便后续使用。

## 主要功能

### Cache 类
**用途**: 基于文件的缓存管理类，支持数据的存储、获取和持久化

**属性**:
- `fp`: 文件操作对象，指向缓存文件
- `store`: 字典类型的数据存储容器

**主要方法**:
- `__init__(name)`: 初始化缓存，指定缓存名称
  - 自动创建 `data/cache/{name}.json` 文件
  - 如果文件存在，会读取已有数据到内存
- `set(key, value)`: 设置缓存键值对
  - 返回 self 支持链式调用
- `get(key)`: 获取指定键的值
- `exists(key)`: 检查键是否存在
- `save()`: 将内存中的数据保存到文件
  - 返回 self 支持链式调用

### 全局缓存管理
**全局变量**:
- `CACHE: Dict[str, Cache] = dict()` - 全局缓存字典，存储所有已创建的缓存实例

**函数**:
- `get_cache(name)`: 获取或创建缓存实例
  - 如果缓存不存在，自动创建新的 Cache 实例
  - 支持单例模式，避免重复创建

## 使用示例

```python
from common.util.cache import get_cache

# 获取缓存实例
cache = get_cache("user_data")

# 设置缓存
cache.set("user1", {"name": "Alice", "age": 25})
cache.set("user2", {"name": "Bob", "age": 30})

# 获取缓存
user1_data = cache.get("user1")
print(user1_data)  # {"name": "Alice", "age": 25}

# 检查缓存是否存在
exists = cache.exists("user1")  # True

# 保存到文件
cache.save()
```

## 工作原理
1. **文件存储**: 缓存数据以 JSON 格式保存在 `data/cache/` 目录下
2. **内存管理**: 数据同时存储在内存中的字典和文件中
3. **懒加载**: 缓存实例创建时自动读取文件数据
4. **全局管理**: 通过全局字典确保同一缓存名称只创建一个实例

## 依赖关系
- `.fp.File` - 文件操作类
- `typing.Dict` - 类型提示

## 测试文件
无对应的测试文件

## 修改注意事项
1. 缓存文件路径固定为 `data/cache/`，确保目录存在
2. 数据序列化为 JSON 格式，确保数据可序列化
3. 全局缓存实例会一直存在内存中，注意内存使用
4. 修改数据后需要调用 `save()` 方法持久化到文件