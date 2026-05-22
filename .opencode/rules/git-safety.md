# Git 安全规则

## 切换分支前的安全检查

- **执行 `git checkout` 切换分支前，必须先检查 `git status`**
- **如果存在未提交的修改，必须先使用 `git stash` 暂存**
  ```bash
  git stash push -m "切换分支前保存修改"
  git checkout <目标分支>
  # 完成操作后
  git checkout <原分支>
  git stash pop
  ```
- 如果有未提交修改，切换分支前必须提醒用户风险

## 重置操作的安全检查

- **执行 `git reset --hard` 前，必须警告用户会永久丢失未提交的修改**
- 建议先 `git stash` 或提交后再执行重置

## Git 操作通用规则

### 破坏性命令执行前必须获得用户确认

以下命令执行前必须先询问用户确认：

| 命令 | 风险说明 |
|------|----------|
| `git reset --hard` | 强制重置，丢失所有未提交修改 |
| `git clean -fd` | 删除未跟踪的文件 |
| `git push --force` | 强制推送，可能覆盖远程历史 |
| `git checkout`（存在未提交修改时） | 切换分支可能导致修改丢失 |
| `git checkout -- <file>` | 用仓库版本覆盖工作区文件 |

### 保护未提交工作

- **始终保护用户的未提交工作，优先使用 `git stash` 而非丢弃**
- 执行任何可能丢失数据的操作前，先备份重要内容

## 操作流程示例

### 安全切换分支流程

```bash
# 1. 先检查状态
git status

# 2. 如果有未提交修改，先暂存
git stash push -m "切换分支前保存修改"

# 3. 切换分支
git checkout <目标分支>

# 4. 完成后返回原分支
git checkout <原分支>

# 5. 恢复暂存的修改
git stash pop
```

### 安全重置流程

```bash
# 1. 先检查状态，确认是否有重要修改
git status

# 2. 如果有重要修改，先暂存或提交
git stash push -m "重置前保存修改"

# 3. 执行重置（需用户确认）
git reset --hard <commit>

# 4. 如需要，恢复暂存
git stash pop
```