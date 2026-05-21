---
description: 本地验证 LeetCode 题目解答
---

你正在执行 `/lc/check` 命令。参数说明：

1. `$1` — 题目编号，必填。如 `2770`、`1674`
2. `$2` — 测试用例名称，可选。未提供时运行所有已缓存的测试用例

执行流程：

1. **定位代码文件**：`app/yly/algo/todo/lc_$1.py`
2. **加载缓存数据**：从 `data/lc/<title_slug>.json` 获取测试用例
   - 若缓存不存在，调用 `LeetCode.prepare_submit()` 获取题目详情并缓存
3. **运行本地测试**：
   - 动态加载 `Solution` 类和目标方法
   - 对每个测试用例执行验证，输出结果和预期值对比
4. **返回测试结果**：`passed` 或 `failed`，附带详细信息

错误处理：

- **LeetCode session 过期**：提示 `"LeetCode 登录已过期，请更新 config/setting/api.json 中的 cookie"`
- **代码文件不存在**：提示 `"请先实现 lc_$1.py"`
- **方法未实现**：提示 `"方法返回空值，请实现解题逻辑"`

遵循规则：

- 使用 `LeetCode.test_local()` 执行测试
- 日志输出到 `data/log/run.log`
- 测试结果打印简洁摘要