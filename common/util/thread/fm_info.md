# FmInfo 模块文档

## 文件概述
`fm_info.py` 提供了一个调用帧信息处理类 `FmInfo`，用于访问和提取 Python 调用帧中的局部变量信息，主要用于调试和线程分析。

## 主要功能

### FmInfo 类
**用途**: 封装 Python 调用帧信息，提供局部变量访问功能

**属性**:
- `frame: FrameType` - Python 调用帧对象

**构造函数**:
- `__init__(self, frame)`: 初始化帧信息对象
  - `frame`: Python 调用帧对象（来自 `inspect` 模块）

**主要方法**:
- `get_local_self()`: 获取局部变量中的 `self`
  - 返回调用帧中 `self` 变量的值
  - 主要用于实例方法的调试

## 使用示例

```python
import inspect
from common.util.thread.fm_info import FmInfo

class MyClass:
    def method(self):
        # 获取当前调用帧
        frame = inspect.currentframe()
        
        # 创建帧信息对象
        fm_info = FmInfo(frame)
        
        # 获取 self 对象
        self_obj = fm_info.get_local_self()
        print(f"Self object: {self_obj}")
        
        # 清理引用循环
        del frame

# 使用示例
obj = MyClass()
obj.method()
```

## 应用场景
- **调试工具**: 在调试过程中访问对象的局部状态
- **线程分析**: 分析多线程环境中的对象状态
- **动态代理**: 在运行时获取对象信息
- **日志记录**: 记录方法调用时的对象状态

## 实现原理
- 使用 Python 的 `types.FrameType` 类型封装调用帧
- 通过 `frame.f_locals` 访问局部变量字典
- 专门提取 `self` 变量，因为这是最常见的调试需求

## 依赖关系
- `types.FrameType` - Python 调用帧类型

## 测试文件
无对应的测试文件

## 修改注意事项
1. 调用帧对象会形成引用循环，使用后需要手动清理
2. `self` 变量可能不存在于所有调用帧中（如静态方法）
3. 在多线程环境中使用时需要注意线程安全
4. 调用帧信息可能包含敏感数据，生产环境使用时要注意安全
5. 该功能主要用于开发和调试，不建议在生产环境中使用