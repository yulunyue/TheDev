# ThreadPoll 模块文档

## 文件概述
`thread_poll.py` 提供了一个线程池管理器 `ThreadManage`，用于批量管理线程任务执行，支持任务创建、提交和结果收集功能。

## 主要功能

### ThreadManage 类
**用途**: 线程池管理器，简化批量任务的线程管理

**属性**:
- `executor: ThreadPoolExecutor` - 线程池执行器

**构造函数**:
- `__init__(self, max_workers=100)`: 初始化线程管理器
  - `max_workers`: 最大工作线程数，默认为 100

**主要方法**:

**任务创建**:
- `get_task(self, func, args)`: 创建任务列表
  - `func`: 要执行的函数
  - `args`: 参数列表
  - 返回: `ThreadExec` 对象列表

**批量执行**:
- `run(self, func, args)`: 批量执行任务
  - `func`: 要执行的函数
  - `args`: 参数列表
  - 创建任务并提交到线程池
  - 等待所有任务完成并收集结果
  - 返回: 所有任务的结果列表

## 使用示例

```python
from common.util.thread.thread_poll import ThreadManage

# 创建线程管理器
thread_manager = ThreadManage(max_workers=4)

# 定义任务函数
def square(x):
    return x * x

# 准备参数列表
args = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 批量执行任务
results = thread_manager.run(square, args)
print(results)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 使用不同的任务函数
def power(x, n):
    return x ** n

args = [(2, 3), (3, 2), (4, 2), (5, 1)]
results = thread_manager.run(lambda args: power(*args), args)
print(results)  # [8, 9, 16, 5]
```

## 工作流程
1. **线程池创建**: 创建指定大小的线程池
2. **任务创建**: 为每个参数创建 `ThreadExec` 任务对象
3. **任务提交**: 将所有任务提交到线程池
4. **异步执行**: 线程池并行执行所有任务
5. **结果收集**: 按完成顺序收集任务结果

## 性能特点
- **并行执行**: 多个任务同时执行，提高效率
- **自动管理**: 线程池自动管理线程的创建和销毁
- **结果有序**: 按任务完成顺序返回结果，不是提交顺序
- **资源复用**: 线程复用，减少创建销毁开销

## 依赖关系
- `concurrent.futures.ThreadPoolExecutor, as_completed` - 线程池和完成迭代
- `typing.List` - 类型提示
- `time, sys` - 系统模块
- `.thread_exec.ThreadExec` - 线程执行器

## 测试文件
无对应的测试文件

## 修改注意事项
1. 线程池大小需要根据任务类型和系统资源配置
2. CPU 密集型任务线程数不宜过多
3. I/O 密集型任务可以适当增加线程数
4. 长时间运行的任务需要考虑超时设置
5. 任务函数应该是无状态的，避免共享可变数据
6. 异常处理应该在任务函数内部完成
7. 可以扩展支持任务优先级和取消功能