---
description: CI/CD — 远端解压安装发布包
---

你正在执行 `/cid/install` 命令。

## 参数

- `$1` — 远端地址，可选。格式 `IP:PORT`，默认 `1.14.97.154:10001`

## 功能

通知远端服务器解压已上传的 `data/upload/the_dev.zip` 到工作目录。

## 执行方式

**优先使用现有工具**（推荐）：
```bash
python tool/service/cli.py install production name=Api ip_port=$1
```
- 如 `$1` 未提供，使用默认 `1.14.97.154:10001`

**手动调用 API**（备选）：
```bash
curl -X POST "http://{ip_port}/app/manage/unzip" \
  -H "Content-Type: application/json" \
  -d '{"path": "data/upload/the_dev.zip"}'
```

## 验证

确认 API 返回成功状态。
