# CubeAction

## 2026-05-13
- `show()` 改为 `"{xyz}轴 第{n}层 {顺/逆时针90°/180°}旋转"` 格式（如 `"y轴 第0层 顺时针90°旋转"`）
- 使用 `self.axis`(`0=y`, `1=x`, `2=z`)、`self.layer_id`、`self.rotate` 构建描述

## 2026-05-11

- `show()` 移除 `src:...dst:...action:...` 前缀，只返回旋转描述（如"第0层B色-顺时针旋转1圈"）。
   不再调用 `super().show(msg)`，避免继承父类 Action 的 `src`/`dst`/`action` 格式。
- 前端 title 和 action_pre（日志）中不再显示 src/dst。
