# cube_3d.ts — Three.js 3D魔方组件

## 2026-05-11 新建

- 使用 Three.js + OrbitControls 实现 3D 魔方渲染
- **8个 Cubie**：每个是 `Mesh`（`BoxGeometry` + 6个 `MeshStandardMaterial`），位于 `(x-0.5, y-0.5, z-0.5)`
- **GRID_MAP**：将后端 24 个 grid 索引映射到 3D 位置 `(x,y,z)` 和面朝向 `(+X/-X/+Y/-Y/+Z/-Z)`，基于 `to_str()` 展开布局推导
- **`set_cube_data(grid, n)`**：更新所有贴片颜色
- **`animate_rotate(axis, layer, rotate, onDone)`**：
  - 按 axis（0=X, 1=Y, 2=Z）+ layer（0/1）找到 4 个 cubie
  - 临时 reparent 到 pivot Group，`slerp` 旋转 300ms（smoothstep 缓动）
  - 完成后回置到 scene，更新 cubie 坐标
- **旋转方向**：CW（rotate=1）对照后端 MOVE_ACTION，分 axis+layer 确定 ±PI/2
- **OrbitControls**：鼠标拖拽旋转视角，阻尼 0.1
- 初始隐藏（`hide()`），由父组件 `toggle_view()` 控制显隐
