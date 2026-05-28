---
description: 查看 LeetCode 题目描述和代码模板
---

你正在执行 `/lc/read` 命令。参数说明：

1. `$1` — 题目编号，必填。如 `2770`、`1674`
2. `$2` — `--fresh`，可选。强制重新拉取题目数据，不使用本地缓存

执行流程：

1. **查询题目信息**：调用 `LcClient.query_num($1)` 获取题目元数据（titleSlug、标题、难度等）
2. **加载题目详情**：调用 `LcProblemService(client).prepare_submit(titleSlug)` 获取完整题目数据（优先使用 `data/lc/<title_slug>.json` 缓存，缓存不存在或指定 `--fresh` 时从 LeetCode 拉取）
3. **展示内容**：
   - 题号、标题、难度
   - 题目描述（`content`，HTML 格式，转化为纯文本后完整展示，包括所有 Example 和 Constraints，不可截断）
   - **题目描述必须翻译成中文展示**
   - Python3 代码模板（`code_snippet`）
   - 本地代码文件路径：`app/yly/algo/todo/lc_$1.py`
4. **检查本地文件**：若 `app/yly/algo/todo/lc_$1.py` 不存在，提示可调用 `make` 命令创建

错误处理：

- **题目未找到**：提示 `"未找到题目 $1，请检查编号是否正确"`
- **LeetCode session 过期**：提示 `"LeetCode 登录已过期，请更新 config/setting/api.json 中的 cookie"`

遵循规则：

- 使用 `get_lc_service()` 创建 `LcClient` 实例
- 日志输出到 `data/log/run.log`
- 展示结果简洁清晰，突出关键信息
