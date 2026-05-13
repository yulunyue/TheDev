---
description: 从 git 远端拉取代码（默认 origin = gitee）
---

你正在执行 `/git/pull` 命令。参数说明：

1. `$1` — remote 名称，可选。默认 `origin`（gitee）
2. `$2` — branch 名称，可选。默认当前分支

执行流程：

1. `git pull --rebase <remote> <branch>`
2. 有冲突时停止并提示用户手动解决
