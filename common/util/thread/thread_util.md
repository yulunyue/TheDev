# ThreadUtil 模块文档

## 文件概述
`thread_util.py` 提供了高级线程工具类 `ThreadRecord`，支持线程执行记录、调试追踪和数据可视化功能，主要用于线程调试和状态监控。

## 主要功能

### ThreadRecord 类
**用途**: 线程执行记录器，支持执行追踪、状态监控和可视化

**继承关系**:
- `threading.Thread` - Python 线程基类

**属性**:
- `error_msg: str` - 错误信息
- `result` - 执行结果
- `state: int` - 线程状态（0: 运行中, 1: 已完成）

**主要方法**:

**生命周期管理**:
- `init(self)`: 初始化方法（可重写）
  - 子类可以重写此方法进行自定义初始化
- `run(self) -> None`: 线程运行方法
  - 设置全局追踪器
  - 执行主逻辑
  - 异常处理和状态管理
- `exec(self)`: 执行主体逻辑
  - 调用 `exec_main()` 方法
  - 子类可以重写此方法

**执行追踪**:
- `globaltrace(self, frame, event, arg)`: 全局追踪器
  - 设置局部追踪器
- `localtrace(self, frame, event, arg)`: 局部追踪器
  - 监控指定键的值变化
  - 记录值变化到 `records` 列表

**状态监控**:
- `set_layout(self, keys)`: 设置监控布局
  - `keys`: 要监控的键列表
  - 记录初始值用于后续比较
- `get_current_value(self, key)`: 获取当前值
  - 支持自定义的 `thread_current_view` 方法
- `get_records(self)`: 获取执行记录
  - 返回值变化记录列表

**执行控制**:
- `execute(self, *args, **kw) -> "ThreadRecord"`: 执行线程
  - 初始化记录列表和消息列表
  - 启动线程并等待完成
  - 返回 self 支持链式调用
- `exec_main(self, *args, **kw)`: 执行主逻辑
  - 调用 `ins.exec()` 方法

**可视化功能**:
- `cli(self, path="data/log/thread_view.log", *args, **kw)`: 命令行界面
  - 支持交互式查看执行过程
  - 使用箭头键浏览执行记录
- `get_layout(self)`: 获取布局显示
  - 生成网格化的数据可视化

## 使用示例

```python
from common.util.thread.thread_util import ThreadRecord

class MyTask(ThreadRecord):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.data = []
    
    def exec(self):
        for i in range(5):
            self.counter += 1
            self.data.append(i)
            time.sleep(0.1)

# 创建并执行任务
task = MyTask()
task.set_layout(["counter", "data"])
result = task.execute()

# 获取执行记录
records = task.get_records()
print(records)  # 记录 counter 和 data 的变化

# 使用命令行界面
# task.cli()
```

## 高级功能

### 执行追踪
- 使用 `sys.settrace()` 设置全局追踪器
- 监控指定变量的值变化
- 记录完整的执行历史

### 数据可视化
- 支持网格化的数据显示
- 集成 PyGraphViz 进行图形可视化
- 提供交互式命令行界面

### 状态管理
- 线程状态实时监控
- 异常捕获和错误记录
- 支持优雅的线程终止

## 依赖关系
- `sys, threading, time` - 系统和线程模块
- `traceback` - 异常跟踪
- `..fp.File` - 文件操作
- `..log.logger` - 日志记录
- `.fm_info.FmInfo, FrameType` - 帧信息
- `math` - 数学计算
- `common.tool.export.FontBase, Row, Column, to_web_view` - 可视化组件
- `common.third_util.pynut_util.PU_UTIL` - 工具集

## 测试文件
无对应的测试文件

## 修改注意事项
1. 全局追踪会影响性能，生产环境建议关闭
2. 监控的键应该是对象的属性，不能是局部变量
3. 值变化比较使用严格相等，复杂对象可能需要自定义比较逻辑
4. 命令行界面依赖外部工具库，使用前需要确保安装
5. 线程执行是异步的，需要等待完成才能获取结果
6. 异常处理会记录堆栈信息，可能包含敏感数据
7. 可以扩展支持更多数据类型和可视化方式