# Export 模块文档

## 文件概述
`export.py` 是一个核心的导出模块，集中了项目中各种常用的功能接口，包括日志、模块、工具、测试、缓存、线程、API、IO 等多个子系统的统一导出。

## 主要功能

### 核心组件导入
该模块统一导出了以下子系统的核心功能：

**日志系统**:
- `get_log, Logger, TheDevLoger` - 日志记录器
- `log, get_dev_log, log1, log2` - 日志函数
- `logger, LOGER_PREFIX` - 全局日志对象

**模块系统**:
- `Module, get_function_info, get_file_path_by_cls` - 模块管理
- `run_catch_error` - 异常捕获和错误处理

**工具函数**:
- `uid, hash_any_str, json_dumps, dict_to_str` - 基础工具
- `ii, md5, base64_encode, base64_decode` - 编码工具
- `url_to_json, url_parse, cmd_parse` - URL 和命令解析
- `SYS_ARGS, SYS_KW, assert_dict, asset_exception` - 系统工具

**测试框架**:
- `TestBase, logger` - 测试基类
- `File` - 文件操作
- `get_cache` - 缓存管理

**线程管理**:
- `ThreadManage, ThreadExec` - 线程池和执行器
- `ThreadRecord` - 线程记录和调试

**数据结构**:
- `ListUtil` - 列表工具
- `Node, search_cls, enum_cls` - 节点和枚举工具

**API 系统**:
- `ApiCall, ApiBase` - API 调用和基类
- `TcpServer, TcpClient, TempFile` - 网络通信

**IO 系统**:
- `TcpServer, TcpClient, TempFile` - TCP 通信
- `IO_MANAGE` - IO 管理

### 全局变量
- `inf = float("inf")` - 无穷大
- `null = None` - None 的别名
- `true, false = True, False` - 布尔值的别名

## 使用示例

```python
from common.util.export import (
    logger, get_log, json_dumps, uid, 
    ThreadManage, ThreadRecord, ApiCall
)

# 使用日志
logger.info("Hello World")
log = get_log("test")
log.debug("Debug message")

# 使用工具函数
data = {"key": "value"}
json_str = json_dumps(data)
unique_id = uid("test")

# 使用线程池
thread_manager = ThreadManage(max_workers=5)
results = thread_manager.run(func, args_list)

# 使用线程记录
record = ThreadRecord()
result = record.execute(some_object)

# 使用API调用
api = ApiCall()
api.register("endpoint", function)
result = api.call("endpoint", params, env)
```

## 模块结构
```
export.py
├── 日志系统 (from .log)
├── 模块系统 (from .module)  
├── 工具函数 (from .tool)
├── 测试框架 (from .test, .fp, .cache)
├── 线程管理 (from .thread.thread_poll)
├── 数据结构 (from .list_util, .node)
├── API 系统 (from .api.apicall, .io.export)
└── 全局变量和类型提示
```

## 依赖关系
该模块是项目的核心导出模块，依赖了以下子模块：
- `.log` - 日志系统
- `.module` - 模块管理
- `.tool` - 工具函数
- `.test` - 测试框架
- `.fp` - 文件操作
- `.cache` - 缓存系统
- `.thread.thread_poll` - 线程池
- `.list_util` - 列表工具
- `.node` - 节点工具
- `.api.apicall` - API 调用
- `.io.export` - IO 导出
- `.constant` - 常量定义
- `.mock` - 模拟工具

## 测试文件
无对应的测试文件

## 修改注意事项
1. 该模块是项目的核心入口，修改时需要考虑向后兼容性
2. 新增导入时需要确保被导入的模块可用
3. 移除导入时需要检查项目其他地方是否使用
4. 全局变量的修改会影响整个项目
5. 导入顺序可能影响模块的初始化顺序
6. 建议在添加新功能时遵循现有的导入结构