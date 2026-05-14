---
description: CI/CD — 远端重启服务
---

你正在执行 `/cid/restart` 命令。

## 参数

- `$1` — 配置环境，可选。默认 `production`
- `$2` — 远端地址，可选。格式 `IP:PORT`，默认 `1.14.97.154:10001`

## 功能

通知远端服务器以指定配置重启 Tornado 服务。

## 执行方式

**优先使用现有工具**（推荐）：
```bash
python tool/service/cli.py restart $1 name=Api ip_port=$2
```
- 如 `$1` 未提供，默认 `production`
- 如 `$2` 未提供，默认 `1.14.97.154:10001`

**手动调用 API**（备选）：
```bash
curl -X POST "http://{ip_port}/app/manage/restart" \
  -H "Content-Type: application/json" \
  -d '{"config": "production"}'
```

## 验证

确认 API 返回成功，远端服务已重新加载。
