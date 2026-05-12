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

### 2026-05-11 新增 block_size 属性

- 新增 `block_size` 属性，默认 50
- 新增 `set_block_size(size)` 方法
- `render_cube` 中 `blockSize` 改用 `this.block_size`
- 便于手机端复用，缩小方块尺寸

### 2026-05-11 颜色调整

- 橙 `#e67e22` → `#ff9800`（亮橙）
- 红 `#e74c3c` → `#d32f2f`（深红）
- 解决红橙颜色接近难以区分的问题

### 2026-05-11 黄色→黑色

- 黄 `#f1c40f` → `#1a1a1a`（黑色），配合3D视觉效果

### 2026-05-12 面内部方向修正

- 新增 `reorderIdx()` 函数
- 背面（face 3）：水平镜像（左右列互换）— 已验证正确
- 左面（face 4）：90° 顺时针旋转 — 修正内部块方向
- 底面（face 5）：90° 顺时针旋转 — 替代原来的竖直镜像
