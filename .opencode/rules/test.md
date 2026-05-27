# 测试规范

## 强制规则

**禁止使用测试替身技术**：
- 禁止 Mock 框架（`unittest.mock`、`pytest-mock`）
- 禁止 Fake 对象（手动覆写实例属性、继承覆写）
- 禁止注入测试专用函数

**使用真实依赖**：
- 启动真实服务（本地端口）
- 使用真实数据库/文件系统
- 测试实际行为而非模拟行为

## 冗余测试

**禁止冗余测试**：
- 同一功能不写多个测试文件（如 `test_agent.py` 和 `agent_test.py`）
- 同一断点不重复验证
- 上游测试通过的路径，下游测试不再覆盖

**测试分层**：

| 层级 | 测试范围 | 说明 |
|------|---------|------|
| 单元测试 | 单个函数/类 | 验证核心逻辑 |
| 集成测试 | 多组件协作 | 验证交互流程 |
| E2E 测试 | 完整链路 | 验证用户场景 |

各层独立，不交叉覆盖。

## 集成测试

**定位**：验证多组件协作，不是验证单个组件功能

**规则**：
- 测试组件间交互（消息传递、状态同步、错误传播）
- 不重复单元测试已覆盖的逻辑
- 使用真实依赖，不隔离组件

**示例**：
```python
# 集成测试：验证 Agent 执行 → WebSocket 推送 → 客户端接收
def test_exec_to_ws_flow(self):
    # 启动真实 Agent 服务
    # 启动真实 WebSocket 服务
    # 执行命令，验证端到端消息流
```

## 命名约定

| 场景 | 命名模式 | 示例 |
|------|---------|------|
| 异常场景 | `test_xxx_no_yyy` | `test_exec_no_agent` |
| 成功场景 | `test_xxx_success` | `test_register_success` |
| 连续操作 | `test_sequential_xxx` | `test_sequential_exec` |
| 异常恢复 | `test_xxx_recover` | `test_exit_recover` |

## 状态清理

每个测试用例必须清理副作用：

```python
def test_xxx(self):
    try:
        # 测试逻辑
    finally:
        IO_MANAGE.io_map.pop("test-key", None)
```

或使用 `setup/teardown`：

```python
def _teardown(self):
    IO_MANAGE.io_map.clear()
```

## 资源隔离

- **端口**：不同测试类使用不同端口区间
- **实例标识**：使用唯一标识符（如 `test-{功能名}`）
- **时间等待**：使用轮询 + 超时，而非固定 `sleep`

## 辅助函数

重复逻辑抽取为模块级函数：

```python
def _wait_for_done(agent_id, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        # 轮询逻辑
        time.sleep(0.05)
```