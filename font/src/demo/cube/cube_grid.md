## cube_grid.ts 变动记录

### 2026-05-10 布局优化

- 方块 40px → 50px，增加视认性
- 移除方块内颜色字母 (`set_html`)，纯色块更干净
- 增加 `boxShadow`（内阴影 + 外阴影），模拟立体感
- 增加 6 个面标签（上/左/前/右/後/下）
- 容器增加 `boxShadow` 和 `borderRadius: 12px`，卡片化
- 修复 faceContainer 中 Row/Column 方向使用错误
- 修复 topRow/midRow/bottomRow 为 Column（水平 flex），使面横向排列

### 2026-05-10 样式规范化

- 容器 `set_style` 从 `init_node` 移到 `init_style`
- 符合 AGENTS.md 规则：所有 `set_style` 集中在 `init_style` 管理
