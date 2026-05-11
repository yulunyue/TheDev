# CubeAction

## 2026-05-11

- `show()` 移除 `src:...dst:...action:...` 前缀，只返回旋转描述（如"第0层B色-顺时针旋转1圈"）。
  不再调用 `super().show(msg)`，避免继承父类 Action 的 `src`/`dst`/`action` 格式。
- 前端 title 和 action_pre（日志）中不再显示 src/dst。
