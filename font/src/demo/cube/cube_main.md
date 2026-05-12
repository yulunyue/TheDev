## cube_main.ts 变动记录

### 2026-05-10 布局重构

- CubeMain 从 `extends Column` 改为 `extends Row`（垂直 flex），适配新布局
- 布局改为**左右两栏**：左侧魔方网格（居中，flex:1）+ 右侧控制面板（320px 固定宽）
- 右侧面板（Row）垂直排列：控制表单 → 按钮行 → 操作日志
- 按钮行（Column 水平排列）：新建/打乱/旋转/求解
- 增加整体背景色 `#e8ecf1`，右面板背景 `#f5f5f5`
- 标题栏增加底部边框，白色背景
- 控制表单增加 `boxShadow` 卡片化
- 动作日志 `Pre` 增加圆角边框、等宽字体、滚动条
- 清理未使用的 import

### 2026-05-10 样式规范化

- `init_node` 中移除所有 `set_style` 调用，全部集中到 `init_style`
- `right_panel`、`left_panel`、`main_body` 改为类成员，以便在 `init_style` 中设置样式
- 符合 AGENTS.md 规则：构造只放在 `init_node`，样式只放在 `init_style`

### 2026-05-11 2D/3D 切换

- 新增 `Cube3D` 导入
- 新增 `cube_3d`、`toggle_btn`、`is_3d` 成员
- 按钮行增加"3D"切换按钮
- `toggle_view()`：`hide()`/`show()` 切换 CubeGrid / Cube3D
- `handle_rotate`：3D 模式下额外调用 `cube_3d.animate_rotate`
- `animate_step`：3D 模式下用 `animate_rotate` 做旋转动画（300ms），2D 模式沿用瞬切
- `update_state`：同时更新 cube_grid 和 cube_3d

### 2026-05-12 Grid API 适配

- `current_state` 字段移除，改用 `current_grid` 数组
- `handle_rotate` 传参 `state` → `grid`
- `handle_solve` 传参 `state` → `grid`
- `update_state` 从 `data.grid` 读取，不再读取 `data.state`
