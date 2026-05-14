---
description: CI/CD — 一键发布现网（build → package → upload → install → restart）
---

你正在执行 `/cid/cicd` 命令。

## 参数

- `$1` — 配置环境，可选。默认 `production`
- `$2` — 远端地址，可选。格式 `IP:PORT`，默认 `1.14.97.154:10001`

## 功能

一键执行完整发布流水线：
1. **build** — 前端生产构建
2. **package** — 打包发布文件
3. **upload** — 上传到远端
4. **install** — 远端解压安装
5. **restart** — 远端重启服务

## 执行方式

**优先使用现有工具**（推荐）：
```bash
python tool/service/cli.py cicd $1 name=Api ip_port=$2
```
- 如 `$1` 未提供，默认 `production`
- 如 `$2` 未提供，默认 `1.14.97.154:10001`

**手动逐步执行**（备选，每步确认）：

1. **构建前端**：
   ```bash
   cd font && npm run build
   ```

2. **打包**：
   ```python
   from common.util.export import File
   File("./").zip(
       "data/the_dev.zip",
       targets=["font/dist", "common", "app/tool", "app/yly", "tool", "main.py", "config/setting/production.json"],
       ignores=[".*__pycache__"],
   )
   ```

3. **上传**（base64 分片，32768 字节/片）：
   - 读取 `data/the_dev.zip` 编码为 base64
   - 逐片 POST 到 `http://{ip_port}/app/manage/post_files_base64`
   - body: `{"path": "data/upload/the_dev.zip", "data": "<chunk>", "cur_idx": N, "last_idx": M}`

4. **远端安装**：
   ```bash
   curl -X POST "http://{ip_port}/app/manage/unzip" \
     -H "Content-Type: application/json" \
     -d '{"path": "data/upload/the_dev.zip"}'
   ```

5. **远端重启**：
   ```bash
   curl -X POST "http://{ip_port}/app/manage/restart" \
     -H "Content-Type: application/json" \
     -d '{"config": "production"}'
   ```

## 遵循规则

- 任一步骤失败立即停止，输出错误信息
- 说明失败原因和建议修复方案
- 上传前向用户确认远端地址和配置环境
- 打包前确认 `font/dist/` 已存在（如不存在自动执行 build）
