---
description: 一键部署 CICD 流水线（构建→打包→上传→解压→重启）
---

你正在执行 `/cli/cicd` 命令。

参数：
- `$1` — 服务端标识，可选，默认 `bolun`
- `$2` — 配置环境名称，可选，默认 `production`

对应方法：`Cli.cicd()`（`tool/service/cli.py:69`）

执行流程（按顺序执行）：
1. `npm_build` — 前端构建（`font/dist`）
2. `install` — 打包→上传→远端解压
3. `restart` — 远端以指定配置重启

**遵循规则**：
- 步骤失败则终止后续流程
- 部署后用 `curl -s -o /dev/null -w "%{http_code}" http://<ip>:<port>/` 确认远端返回 200
- 默认 `production` 配置对应端口 10000（管理端 10001）
