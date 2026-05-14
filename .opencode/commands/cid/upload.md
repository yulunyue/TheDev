---
description: CI/CD — 上传发布包到远端（base64 分片）
---

你正在执行 `/cid/upload` 命令。

## 参数

- `$1` — 远端地址，可选。格式 `IP:PORT`，默认 `1.14.97.154:10001`
- `$2` — 分片大小，可选。默认 `32768`（8192×4）

## 功能

将 `data/the_dev.zip` 以 base64 分片方式上传到远端服务器的 `/app/manage/post_files_base64` 端点。

## 执行方式

**优先使用现有工具**（推荐）：
```bash
python tool/service/cli.py upload_base_64 production name=Api ip_port=$1 b64_pkg_num=$2
```
- 如 `$1` 未提供，使用默认 `1.14.97.154:10001`
- 如 `$2` 未提供，使用默认 `32768`

**手动调用 API**（备选）：
1. 读取 `data/the_dev.zip` 并编码为 base64
2. 按 `b64_pkg_num` 分片
3. 逐片 POST 到 `http://{ip_port}/app/manage/post_files_base64`，body：
   ```json
   {"path": "data/upload/the_dev.zip", "data": "<chunk>", "cur_idx": N, "last_idx": M}
   ```
4. 每片上传后打印进度

## 验证

- 所有分片上传无报错
- 确认服务端返回非 HTML 错误页
- 输出最终文件 MD5
