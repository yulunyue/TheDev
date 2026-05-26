# Python 代码规范

## 强制规则

1. **Black 格式化**：所有 Python 文件必须通过 `black --check`
2. **导入规则**：
   - util 层 → `common.util.export`
   - tool 层 → `common.tool.export`
3. **文件结构**：一个文件只有一个类，类名与文件名一致
4. **行数限制**：
   - 文件行数 ≤ 300 行，超过需拆分模块
   - 函数行数 ≤ 50 行，超过需拆分子函数
5. **参数限制**：函数参数 ≤ 5 个，超过需用 `**kwargs` 或配置对象

## 检查命令

```bash
python -m black --check <目录>  # 检查格式化
python -m black <目录>          # 执行格式化
python -m pytest tests/         # 运行测试
```

## 重构流程

1. 分析源文件结构 → 检查行数、参数个数
2. 设计重构计划 → 确认规则符合性
3. 写入新文件 → 控制文件行数 ≤ 300，函数行数 ≤ 50
4. **执行 Black 格式化**（强制）
5. **执行导入检查**（强制）
6. 运行测试验证

## 导入规则详解

| 层级 | 导入来源 | 典型导出 |
|------|---------|---------|
| util 层 | `common.util.export` | `File`, `logger`, `Node`, `ApiBase`, `C`, `TestBase`, `Module` |
| tool 层 | `common.tool.export` | `GC`, `OsUtil`, `ToolBase`, `System`, `ProcessLock`, `PyUtil`, `FrontTable` |

**禁止跨层导入**：`util/export.py` 不导出 `tool` 层的类，反之亦然。