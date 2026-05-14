---
description: CI/CD — 前端构建（font/dist）
---

你正在执行 `/cid/build` 命令。

## 功能

前端生产构建，生成 `font/dist/` 目录。

## 执行流程

1. 删除旧的 `font/dist/` 目录（如存在）
2. 切换到 `font/` 目录执行构建：
   ```bash
   cd font && npm run build
   ```
3. 确认 `font/dist/` 目录已生成且包含构建产物

## 错误处理

- npm 报错时输出完整日志
- 构建失败不要继续后续步骤
