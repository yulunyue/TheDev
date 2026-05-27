---
description: 提交 LeetCode 解答并查看评测结果
---

你正在执行 `/lc/submit` 命令。参数说明：

1. `$1` — 题目编号，必填。如 `2770`、`1674`
2. `$2` — 提交等待超时秒数，可选。默认 120 秒

执行流程：

1. **验证代码文件**：确认 `app/yly/algo/todo/lc_$1.py` 存在
2. **查询题目信息**：调用 `LcClient.query_num($1)` 获取 titleSlug
3. **读取代码**：从 `app/yly/algo/todo/lc_$1.py` 读取完整代码
4. **提交到 LeetCode**：调用 `LcProblemService(client).submit(titleSlug, code)` 获取 `submission_id`
5. **轮询评测结果**：每 4 秒调用 `LcClient.check(submission_id)` 查询状态，直到出现以下结果：
   - `"Accepted"` → 通过，展示 `passedTestCaseCnt/totalTestCaseCnt`、运行时间、内存
   - `"Wrong Answer"` → 未通过，展示输入、期望输出、实际输出（来自 `outputDetail`）
   - `"Time Limit Exceeded"` → 超时
   - 编译错误或运行时错误 → 展示 `outputDetail.compileError` / `outputDetail.runtimeError`
6. **返回最终结果**：成功或失败的详细信息

错误处理：

- **代码文件不存在**：提示 `"请先实现 lc_$1.py"`
- **提交失败**：提示网络或服务端错误信息
- **超时未出结果**：提示 `"评测超时，请登录 LeetCode 查看结果"`
- **LeetCode session 过期**：提示 `"LeetCode 登录已过期，请更新 config/setting/api.json 中的 cookie"`

遵循规则：

- 使用 `get_lc_service()` 创建 `LcClient` 实例
- 轮询间隔 4 秒，参考 `LcProblem.check()` 的实现
- 日志输出到 `data/log/run.log`
- 结果展示清晰，包含关键统计数据
