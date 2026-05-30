# 后端重启规则

## 背景

当前项目使用 `python -m tool.cli dev` 启动 Tornado 服务器。后端代码修改后，服务器进程需要重启才能生效。

## 强制规则

1. **Python 代码修改后必须重启服务器**
   - 修改 `app/` 目录下任何 `.py` 文件
   - 修改 `common/` 目录下任何 `.py` 文件
   - 修改数据库相关代码（model.py）
   - **必须执行**: `python -m tool.cli dev`

2. **数据库结构变更需要额外处理**
   - 修改 `SqliteDbStore` 子类的字段定义（添加/删除/修改字段）
   - **必须执行**:
     ```bash
     # 1. 停止服务器
     Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force
     
     # 2. 删除旧数据库文件
     Remove-Item "data/werewolf/*.db" -Force
     
     # 3. 重新启动服务器
     python -m tool.cli dev
     ```

3. **测试验证流程**
   - 修改后端代码后，先用 API 测试验证
   - 使用 PowerShell 测试时，必须设置请求头:
     ```powershell
     Invoke-WebRequest -Uri "http://localhost:49999/<api_path>" `
         -Method POST `
         -Body '{"param": "value"}' `
         -ContentType "application/json" `
         -Headers @{"the_dev_user"="<username>"} `
         -UseBasicParsing
     ```
   - **注意**: 请求头 `the_dev_user` 是必需的，否则后端无法识别用户

4. **前端代码修改**
   - 前端 TypeScript 修改后，开发服务器会自动刷新
   - 如果修改涉及新文件，需要在 `app.ts` 中注册路由

## 常见问题

### Q1: 为什么 API 返回 `username` 为空？

**原因**: 请求未设置 `the_dev_user` 请求头

**解决**:
```powershell
-Headers @{"the_dev_user"="test_user"}
```

### Q2: 为什么数据库字段验证失败？

**原因**: `SelectModel` 的选项列表不包含设置的值

**解决**: 
1. 检查 `SelectModel.set_options()` 是否包含目标值
2. 删除旧数据库文件重新创建

### Q3: 前端按钮不显示？

**可能原因**:
1. 后端未返回必要字段（如 `my_info`）
2. 前端判断条件错误（如 `is_host`）
3. localStorage 中没有用户名

**排查步骤**:
1. 用 API 测试验证后端返回
2. 检查前端 `web_dom.get_local_data(Ct.username)`
3. 检查前端判断逻辑

## 重启检查清单

修改以下文件后必须重启：

| 目录 | 文件类型 | 重启必要性 |
|------|---------|-----------|
| `app/werewolf/` | *.py | ✅ 必须 |
| `app/tool/` | *.py | ✅ 必须 |
| `common/util/` | *.py | ✅ 必须 |
| `common/tool/` | *.py | ✅ 必须 |
| `config/setting/` | *.json | ❌ 不需要（动态加载） |
| `font/src/` | *.ts | ❌ 不需要（自动刷新） |

## 数据库变更检查清单

以下变更需要删除数据库文件：

| 变更类型 | 示例 |
|---------|------|
| 添加字段 | `new_field = StrModel()` |
| 删除字段 | 删除已有字段定义 |
| 修改字段类型 | `StrModel()` → `NumberModel()` |
| 修改 `SelectModel` 选项 | `.set_options("a", "b")` → `.set_options("a", "b", "c")` |
| 修改表名 | 添加 `__table_name__` |

## 示例流程

### 添加新的 Role 状态

```bash
# 1. 修改 constant.py - 添加 Role.UNSET
# 2. 修改 model.py - SelectModel 添加 unset 选项
# 3. 修改 engine.py - 过滤 unset 状态

# 4. 重启服务器（必须）
python -m tool.cli dev

# 5. 删除数据库（如果修改了 SelectModel）
Get-Process -Name python | Stop-Process -Force
Remove-Item "data/werewolf/*.db"
python -m tool.cli dev

# 6. 验证
Invoke-WebRequest -Uri "http://localhost:49999/werewolf/lobby/create_room" ...
```