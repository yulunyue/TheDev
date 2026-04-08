# Mock 模块文档

## 文件概述
`mock.py` 提供了测试和调试用的模拟工具类，包括日志模拟、输入输出重定向、测试用例执行框架等功能，主要用于算法题测试和开发调试。

## 主要类和功能

### logger 类
**用途**: 提供空实现的日志记录器，用于测试时屏蔽日志输出

**方法**:
- `info(*args, **kw)` - 空实现的info日志
- `map(*args, **kw)` - 空实现的映射日志
- `debug(*args, **kw)` - 空实现的调试日志
- `log_tree(*args, **kw)` - 空实现的树形日志
- `log_grid(*args, **kw)` - 空实现的网格日志

### CT (Constant Tools) 类
**用途**: 提供数学计算相关的常量和工具函数（与constant.py中的CT类似）

**常量**:
- `MOD = (10**9) + 7` - 模运算常量
- `inf = float("inf")` - 无穷大
- `MX = (10**5) + 1` - 数组大小上限

**工具函数**:
- `min(a, b)` - 返回两个数中的较小值
- `max(a, b)` - 返回两个数中的较大值

### MockCf (Mock Configuration) 类
**用途**: 测试配置和执行的核心类，支持输入重定向、测试用例管理

**属性**:
- `dev = False` - 开发模式标志
- `logger: logger = None` - 日志记录器
- `type = ""` - 类型标识
- `execute = None` - 执行函数
- `cases` - 测试用例字典
- `src_file` - 源文件路径
- `inputs` - 输入列表

**主要方法**:
- `__init__(f=None, cases=None, src=None)` - 初始化配置
- `get_cases() -> Dict` - 获取测试用例
- `set_logger(log)` - 设置日志记录器
- `set_inputs(inputs: str)` - 设置输入字符串
- `input()` - 重定向输入，从inputs列表读取
- `ii()` - 读取一行并转换为整数列表
- `output(s)` - 输出结果到文件
- `run(case_name="")` - 运行测试用例
- `execute(inps: str)` - 执行函数
- `init(**kw)` - 初始化（需子类实现）
- `log(**kw)` - 记录日志
- `get_agent(**kw)` - 获取测试代理（需子类实现）

### MockCg (Mock Configuration Group) 别名
- `MockCg = MockCf` - MockCf的别名，用于分组测试

## 核心函数

### oj_run(ins: "MockCf", case_name=None, with_thread=False)
**用途**: 在线评测运行器，执行测试用例并验证结果

**流程**:
1. 从MockCf实例获取测试用例
2. 为每个用例创建独立日志
3. 获取测试代理或直接执行
4. 比较预期结果和实际结果
5. 输出测试结果
6. 编译源文件到单个文件

### execute_by_thread(ins: MockCf, case: dict)
**用途**: 多线程执行测试用例并记录执行过程

**功能**:
- 初始化测试实例
- 创建线程记录器
- 执行测试并记录方法调用
- 返回布局和执行记录

### exec_thread_recode_file(cls: Callable[[], MockCf], case_name)
**用途**: 执行测试用例并将结果保存到文件

**功能**:
- 创建测试实例
- 执行多线程测试
- 将结果保存为JSON文件

## 使用示例

```python
from common.mock import MockCf, logger, CT

# 创建测试配置
class MyTest(MockCf):
    def __init__(self):
        super().__init__()
        self.cases = {
            "test1": {
                "input": "5",
                "result": [1, 2, 3, 4, 5]
            }
        }
    
    def main(self):
        n = int(self.input())
        return list(range(1, n+1))

# 运行测试
test = MyTest()
test.run("test1")  # 输出: PASS test1 [1,2,3,4,5]==[1,2,3,4,5]
```

## 测试支持
- 支持多测试用例管理
- 支持输入重定向
- 支持结果验证
- 支持多线程执行
- 支持执行过程记录

## 依赖关系
- `json` - JSON数据处理
- `sys` - 系统相关功能
- `functools` - 函数工具
- `heapq` - 堆队列算法
- `typing` - 类型提示
- `math` - 数学函数
- `collections` - 集合数据结构
- `os` - 操作系统接口
- `random` - 随机数生成
- `itertools` - 迭代器工具
- `bisect` - 二分查找算法
- `common.tool.export` - 导出工具
- `common.util.export` - 工具导出

## 修改注意事项
1. 修改日志行为时考虑测试环境需求
2. 输入重定向逻辑要保持稳定
3. 测试用例格式要保持兼容
4. 多线程执行要考虑线程安全
5. 文件操作要注意异常处理