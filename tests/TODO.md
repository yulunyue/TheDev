# 测试待修复事项

## 失败测试统计（约88个）

### 需修复测试（API不匹配）- 约35个

| 文件 | 失败数 | 问题描述 |
|------|--------|----------|
| `test_enum_util.py` | 11 | 测试假设 `EnumCls` 有 `type` 属性，但源码无此属性 |
| `test_difftool.py` | 7 | 测试假设 `Diff.__init__()` 接受 `key_join_char` 参数，但源码只接受 `src` |
| `test_config.py` | 2 | 测试假设 `ConfigBase.insert()` 无参数，但源码需要 `idx` 参数 |
| `form_base_test.py` | 10 | `asset_exception()` 函数期望特定错误消息格式，但实际抛出不同类型 |
| `test_util_tool.py` | 1 | base64 编码断言不匹配 |

### 外部依赖问题 - 约25个

| 文件 | 失败数 | 问题描述 |
|------|--------|----------|
| `test_git_api.py` | 16 | 需要 git 仓库和 git 命令行工具，环境不满足 |
| `test_file_config.py` | 7 | 需要配置文件路径和数据库资源 |
| `test_al.py` | 3 | 需要外部题库文件 `lc_*.py` |
| `test_mctssearch.py` | 1 | 可能依赖 ML 库 |

### 断言格式问题 - 约15个

| 文件 | 失败数 | 问题描述 |
|------|--------|----------|
| `test_cache.py` | 4 | `assert_dict` 比较失败，返回值与期望不符 |
| `test_thread.py` | 1 | 断言值不匹配 |
| `test_export.py` | 1 | 导入检查失败 |

### ML训练测试失败 - 约4个

| 文件 | 失败数 | 问题描述 |
|------|--------|----------|
| `test_ql.py` | - | `TypeError: argument...` 参数类型错误 |
| `test_sarse.py` | - | 同上 |
| `test_value_func.py` | - | 同上 |
| `test_pi_func.py` | - | 同上 |

### 其他 - 约8个

| 文件 | 失败数 | 问题描述 |
|------|--------|----------|
| `str_util_test.py` | 6 | `format_g_tree`, `format_grid` 测试失败 |
| `cube_test.py` | 4 | `rotate/solve/get_state/to_form_column_view` 测试失败 |
| `test_api.py` | 2 | API 加载和返回格式问题 |
| `todo_test.py` | 1 | `todo_insert` 测试失败 |

---

## 处理建议

### 应该修复的测试（源码问题）
- `test_enum_util.py`: 测试与源码 API 不匹配，需更新测试或源码
- `test_difftool.py`: 测试假设了不存在的参数，需更新测试
- `test_config.py`: 测试调用签名错误，需更新测试
- `form_base_test.py`: 错误消息格式不匹配，需更新断言

### 应该标记可选或删除的测试（依赖问题）
- `test_git_api.py`: 外部依赖不可用，应标记为 `@pytest.mark.skipif`
- `test_al.py`: 依赖外部题库文件不存在
- `test_file_config.py`: 需要特定配置资源

### 应该修复源码的测试
- `test_enum_util.py`: 源码 `EnumCls` 缺少 `type` 属性（如果确实需要）
- `test_cache.py`: 源码 `get_cache()` 返回值与期望不符

---

## 测试覆盖缺口（未测试的重要模块）

| 模块 | 重要性 | 建议 |
|------|--------|------|
| `common/third_util/http.py` | 🔴 核心（Tornado 服务器） | 高优先级添加测试 |
| `common/util/node.py` | 🔴 核心（数据模型） | 高优先级添加测试 |
| `common/util/api/apibase.py` | 🔴 核心（API 基类） | 高优先级添加测试 |
| `common/tool/toolbase.py` | ⚠️ 中等 | 添加测试 |
| `common/tool/func/process_lock.py` | ⚠️ 中等 | 添加测试 |
| `common/tool/func/system.py` | ⚠️ 中等 | 添加测试 |
| `common/tool/func/py_util.py` | ⚠️ 中等 | 添加测试 |
| `app/tool/user.py` | ⚠️ 中等 | 添加测试 |

---

## 清理历史

### 2026-05-15 执行清理
- ✅ 删除 `tests/common/util/fp_test.py`（与 `test_fp.py` 重复）
- ✅ 删除 `tests/common/constant_test.py`（与 `test_constant.py` 重复）
- ✅ 删除 `tests/common/util/str_util_test.py` 第217-260行（pytest 重复函数）
- ✅ 更新 `AGENTS.md` 测试规范：`*_test.py` → `test_*.py`
- ✅ 更新 `pytest.ini` 添加命名规范配置