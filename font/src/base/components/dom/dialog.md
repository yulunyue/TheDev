## dialog.ts 变动记录

### 2026-05-10 Dialog 重构：标题栏 + 关闭按钮

- **header** 重构为 flex row 布局，包含 `title_span`（标题）和 `close_btn`（✕ 关闭按钮）
- 移除了 dialog 背景点击关闭（`this.on_click(this.hide.bind(this))`）
- **只有点击 ✕ 按钮才能关闭弹窗**
- 新增 `set_title(title: string)` 方法设置标题
- header 和 main 都阻止事件冒泡，点击不会意外关闭
