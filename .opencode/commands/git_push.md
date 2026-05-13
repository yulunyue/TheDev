---
description: 提交代码并推送到 git 远端（默认 origin + github）
---

你正在执行 `/git_push` 命令。参数说明：

1. `$1` — commit message，可选。未提供时，根据 `git diff --stat` 和 `git diff` 的变更内容，用简洁中文自动生成
2. `$2` — remote 名称，可选。值为 `origin` 或 `github`。**未提供时默认推送到两个远端**

执行流程：

1. 运行 `git status` 确认当前变更
2. 运行 `git diff --stat` 和 `git diff` 查看具体变更
3. **先执行 `git pull --rebase origin <current_branch>` 拉取最新代码**
4. 如已存在 staged 变更则跳过 add，否则**逐个确认后用 `git add <file>` 添加文件**
5. 用 `$1` 或自动生成的 message 执行 `git commit -m "<message>"`
6. **推送**：
   - 无 `$2`：依次推送到 `origin` 和 `github`
   - 有 `$2`：只推送到指定 remote

**遵循规则**：
- 所有 commit message 用中文
- 不要修改 git config
- 禁止使用 `--no-verify`、`--force` 等危险参数
- 不 amend 已推送的 commit
- 如果 rebase 有冲突：
  1. 执行 `git rebase --abort` 放弃 rebase
  2. 创建新分支：`git checkout -b <current_branch>_push_<timestamp>`（timestamp 格式 `YYYYMMDD_HHMMSS`）
  3. 在新分支上执行 `git commit` 和推送