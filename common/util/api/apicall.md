# ApiCall 模块文档

## 文件概述
`apicall.py` 提供了一个 API 调用管理器 `ApiCall`，支持 API 函数注册、动态调用、异常处理和模拟调用等功能。

## 主要功能

### ApiCall 类
**用途**: API 调用管理器，提供统一的 API 接口调用机制

**属性**:
- `fun_map: dict()` - 函数映射表，路径到函数的映射
- `mock_call: list` - 模拟调用列表，用于测试和调试

**主要方法**:

**模拟调用管理**:
- `add_hock(call)`: 添加模拟调用函数
  - 用于测试时的钩子函数
  - 支持多个钩子函数

**核心调用方法**:
- `call_app(path, params, env)`: 应用层 API 调用
  - 检查路径是否存在
  - 设置路由路径和环境变量
  - 执行目标函数
  - 异常处理和错误返回
- `call(path, param, env)`: 完整的 API 调用
  - 包含模拟调用处理
  - 执行应用调用并处理模拟钩子

**API 注册**:
- `register(key: str, fun)`: 注册 API 函数
  - `key`: API 路径
  - `fun`: 函数对象
  - 检查重复注册
  - 记录注册日志

**模块加载**:
- `load_module(module_name_key, cls: ApiBase)`: 加载 API 模块
  - 自动发现类中的 API 方法
  - 支持自定义 API 路由
  - 处理 front_apis 属性
- `load_modules(mds: List[Dict])`: 批量加载模块
  - 支持多个模块配置
  - 路径和模块名映射

## 使用示例

```python
from common.util.api.apicall import ApiCall
from common.util.api.apibase import ApiBase

# 定义 API 类
class UserApi(ApiBase):
    ROUTE_PATH = "/api/user"
    
    def set_env(self, the_dev_user, **kw):
        super().set_env(the_dev_user, **kw)
        return self
    
    def get_user(self, user_id):
        return {"user_id": user_id, "name": "John"}

# 创建 API 调用管理器
api_call = ApiCall()

# 手动注册 API 函数
api_call.register("/api/user/get_user", UserApi().get_user)

# 或者使用模块加载
api_call.load_module("/api/user", UserApi)

# 调用 API
result = api_call.call(
    "/api/user/get_user", 
    {"user_id": 123}, 
    {"the_dev_user": "admin"}
)
print(result)  # {"user_id": 123, "name": "John"}

# 添加模拟调用
def mock_call(path, param, result):
    print(f"Mock call: {path} with {param} -> {result}")

api_call.add_hock(mock_call)
```

## 调用流程
1. **路径检查**: 验证 API 路径是否已注册
2. **实例设置**: 获取 API 实例并设置路由路径
3. **环境配置**: 调用 `set_env` 设置环境变量
4. **函数执行**: 执行目标函数
5. **异常处理**: 捕获异常并返回错误信息
6. **模拟处理**: 执行所有模拟钩子函数

## 错误处理
- **404 错误**: 路径未注册时返回
- **500 错误**: 函数执行异常时返回
- **错误信息**: 包含异常堆栈信息

## 依赖关系
- `..fp.File` - 文件操作
- `..log.logger, get_log, get_dev_log` - 日志记录
- `..module.get_function_info, Module` - 模块管理
- `..tool.uid, json_dumps` - 工具函数
- `..node.Node` - 节点工具
- `typing.List, Dict` - 类型提示
- `json` - JSON 处理
- `os` - 操作系统接口
- `.apibase.ApiBase` - API 基类
- `traceback` - 异常跟踪

## 测试文件
无对应的测试文件

## 修改注意事项
1. API 路径应该是唯一的，重复注册会抛出异常
2. 模拟调用函数的签名应该是 `(path, param, result)`
3. 异常处理会捕获所有异常，包括系统异常
4. 模块加载支持 `#` 开头的路径跳过
5. 环境变量应该在调用前正确设置
6. 函数参数应该与注册的函数签名匹配