# ThreadExec 模块文档

## 文件概述
`thread_exec.py` 定义了线程执行器类 `ThreadExec`，用于封装函数执行任务，支持线程池管理和异步执行功能。

## 主要功能

### ThreadExec 类
**用途**: 线程任务封装器，将函数和参数打包为可执行任务

**属性**:
- `func`: 要执行的函数
- `args`: 函数参数
- `future`: 线程执行结果（Future 对象）

**主要方法**:

**任务配置**:
- `load(self, func, args=None)`: 加载任务配置
  - `func`: 要执行的函数
  - `args`: 函数参数，默认为 None
  - 返回 self 支持链式调用

**线程池执行**:
- `add_to_executor(self, executor: ThreadPoolExecutor)`: 添加到线程池执行
  - `executor`: 线程池执行器
  - 提交任务到线程池
  - 返回 Future 对象用于获取执行结果

## 使用示例

```python
from common.util.thread.thread_exec import ThreadExec
from concurrent.futures import ThreadPoolExecutor

# 创建线程池
executor = ThreadPoolExecutor(max_workers=4)

# 定义任务函数
def task_function(x, y):
    return x + y

# 创建线程执行器
thread_exec = ThreadExec()

# 配置任务
thread_exec.load(task_function, args=(10, 20))

# 添加到线程池执行
future = thread_exec.add_to_executor(executor)

# 获取执行结果
result = future.result()
print(result)  # 30

# 链式调用
future = ThreadExec().load(task_function, args=(5, 5)).add_to_executor(executor)
result = future.result()
print(result)  # 10
```

## 工作流程
1. **任务创建**: 创建 `ThreadExec` 实例
2. **配置任务**: 调用 `load()` 方法设置函数和参数
3. **提交任务**: 调用 `add_to_executor()` 方法提交到线程池
4. **异步执行**: 线程池在后台执行任务
5. **结果获取**: 通过 Future 对象获取执行结果

## 设计特点
- **任务封装**: 将函数和参数封装为可执行对象
- **异步执行**: 支持异步任务提交和结果获取
- **链式调用**: 支持 load 和 add_to_executor 的链式调用
- **线程池集成**: 与 `ThreadPoolExecutor` 无缝集成

## 依赖关系
- `.thread_poll.ThreadPoolExecutor` - 线程池执行器

## 测试文件
无对应的测试文件

## 修改注意事项
1. 任务函数应该是可序列化的，避免使用 lambda 表达式
2. 参数传递使用 `args` 参数，不支持关键字参数
3. Future 对象可以用于取消任务和获取执行状态
4. 线程池大小需要根据实际需求配置
5. 长时间运行的任务需要考虑超时设置
6. 异常处理应该在任务函数内部完成
7. 可以扩展支持关键字参数和回调函数