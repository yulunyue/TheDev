---
description: CI/CD — 打包发布文件（data/the_dev.zip）
---

你正在执行 `/cid/package` 命令。

## 功能

将以下内容打包为 `data/the_dev.zip`：
- `font/dist/` — 前端构建产物
- `common/` — 通用模块
- `app/tool/` — API 处理器
- `app/yly/` — 业务模块
- `tool/` — 工具脚本
- `main.py` — 入口文件
- `config/setting/production.json` — 生产配置

排除 `__pycache__` 目录。

## 执行方式

**优先使用现有工具**（推荐）：
```bash
python tool/service/cli.py package
```

**手动打包**（备选）：
```python
from common.util.export import File
File("./").zip(
    "data/the_dev.zip",
    targets=["font/dist", "common", "app/tool", "app/yly", "tool", "main.py", "config/setting/production.json"],
    ignores=[".*__pycache__"],
)
```

## 验证

确认 `data/the_dev.zip` 文件已生成且非空。
