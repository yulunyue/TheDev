---
description: CI/CD — 远端 Bolun 服务启动
---

你正在执行 `/cid/start` 命令。

## 参数

- `$1` — 配置环境，可选。默认 `production`
- `$2` — 远端地址，可选。格式 `IP:PORT`，默认 `1.14.97.154:10001`

## 功能

通知远端 Bolun 服务器启动 Tornado 服务（适用于首次部署或服务停止后的启动，与 restart 不同：不会先 kill 旧进程）。

## 执行方式

调用远端 API：
```bash
curl -X POST "http://{ip_port}/app/manage/start" \
  -H "Content-Type: application/json" \
  -d '{"config": "production"}'
```
- 如 `$1` 未提供，默认 `production`
- 如 `$2` 未提供，默认 `1.14.97.154:10001`

## 备用方案

如 `/app/manage/start` 端点不存在，使用 `/app/manage/restart` 端点替代：
```bash
curl -X POST "http://{ip_port}/app/manage/restart" \
  -H "Content-Type: application/json" \
  -d '{"config": "production"}'
```

## 验证

确认 API 返回成功，远端端口 9999 已开始监听。
