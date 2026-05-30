---
description: 查看 LeetCode 题目描述和代码模板
---

你正在执行 `/lc/read` 命令。参数说明：

1. `$1` — 题目编号，必填。如 `2770`、`1674`
2. `$2` — `--fresh`，可选。强制重新拉取题目数据，不使用本地缓存

执行流程：

**直接执行**：`python -m tool.service.lc read $1 [$2]`（`$2` 为 `--fresh` 时强制重新拉取）

此命令通过 `tool/service/lc.py` 的 `Lc.read()` 方法完成全部逻辑，包括：
1. 查询题目元数据
2. 加载题目详情（缓存或拉取）
3. 展示内容（题号、标题、难度、中文描述、示例、约束、Python3 模板）
4. 自动创建本地代码文件（如不存在）

错误处理：

- **题目未找到**：提示 `"未找到题目 $1，请检查编号是否正确"`
- **LeetCode session 过期**：提示 `"LeetCode 登录已过期，请更新 config/setting/api.json 中的 cookie"`

遵循规则：

- 日志输出到 `data/log/run.log`
- 展示结果简洁清晰，突出关键信息
