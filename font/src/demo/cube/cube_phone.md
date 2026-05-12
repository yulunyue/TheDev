## cube_phone.ts 变动记录

### 2026-05-11 新建手机端魔方 UI

- 新建 `CubePhone` 类，继承 `Row`（垂直布局）
- 适配移动端：单列纵向布局，方块尺寸 32px
- 简化控制栏：打乱 + 重置 + 求解 三个按钮
- 步数输入使用简单数字框（非 FormRow）
- 动画延迟 200ms，适合移动端性能
- 无旋转表单（保留核心功能）
- 注册到 `app.ts` 路由，通过 `?route=cube_phone` 访问

### 2026-05-11 2D/3D 切换

- 新增 `Cube3D` 导入
- 新增 `cube_3d`、`btn_toggle`、`is_3d` 成员
- 按钮行增加"3D"切换按钮（紫色 `#9b59b6`）
- `toggle_view()`：`hide()`/`show()` 切换 CubeGrid / Cube3D
- `cube_3d` 尺寸 `100%` × `320px`（移动端适配）
- `handle_scramble`/`handle_solve`/`handle_rotate`：3D 模式下用 `animate_rotate` 做旋转动画
- `update_state`：同时更新 cube_grid 和 cube_3d

### 2026-05-12 Grid API 适配

- `current_state` 字段移除，改用 `current_grid`
- 所有 API 请求传参 `state` → `grid`
- `update_state` 从 `data.grid` 读取
