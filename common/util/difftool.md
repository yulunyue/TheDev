# DiffTool 模块文档

## 文件概述
`difftool.py` 提供了一个数据差异比较工具类，支持深度比较两个数据结构并生成详细的差异报告，主要用于测试验证和数据对比。

## 主要功能

### Diff 类
**用途**: 比较两个数据结构的差异，生成可读的差异报告

**属性**:
- `src`: 源数据结构
- `key_join_char`: 键连接符，默认为 "/"
- `diff_result`: 存储差异结果的列表

**主要方法**:
- `__init__(src)`: 初始化差异比较器，设置源数据
- `compare(dst)`: 比较源数据和目标数据，返回差异结果
  - 自动处理 JSON 字符串和字典/列表的转换
  - 生成结构化的差异报告
- `insert(keys, value)`: 记录插入操作的差异
- `delete(keys, value)`: 记录删除操作的差异
- `diff(keys, src, dst)`: 记录修改操作的差异
- `is_same(dst)`: 判断两个数据是否相同
  - 支持字符串和复杂类型的相互转换
  - 返回差异报告字符串，空字符串表示相同
- `expect_ndarray(a, e, wucha=0.000001)`: 比较 numpy 数组
  - 支持梯度张量的自动转换
  - 提供容差参数处理浮点数精度问题

### 核心算法
`diff_any(src, dst, keys)` - 递归比较任意类型的数据：
1. **None 值处理**: 处理 None 值的比较
2. **字典类型**: 递归比较每个键值对
3. **列表类型**: 按索引递归比较元素
4. **基本类型**: 直接比较字符串、数字、布尔值
5. **numpy 数组**: 调用专门的数组比较方法

## 使用示例

```python
from common.util.difftool import Diff

# 创建差异比较器
diff = Diff({"a": 1, "b": {"c": 2}})
target = {"a": 1, "b": {"c": 3, "d": 4}}

# 比较数据
result = diff.compare(target)
print(result)
# 输出类似：
# ['insert[/b/d][4]', 'update[/b/c][2][3]', 'ret:{"a": 1, "b": {"c": 3, "d": 4}}', 'exp:{"a": 1, "b": {"c": 2}}']

# 判断是否相同
is_equal = diff.is_same(target)
print(is_equal)  # 返回差异字符串

# 比较numpy数组
import numpy as np
diff.expect_ndarray(np.array([1.0, 2.0]), np.array([1.000001, 2.000001]))
```

## 差异报告格式
差异报告包含以下操作类型：
- `insert[key_path][value]`: 插入操作
- `delete[key_path][value]`: 删除操作  
- `update[key_path][old_value][new_value]`: 修改操作

## 支持的数据类型
- **基本类型**: str, int, bool, float
- **容器类型**: dict, list
- **特殊类型**: None
- **numpy 数组**: 自动处理梯度张量

## 依赖关系
- `json` - JSON 数据处理
- `typing.List` - 类型提示
- `common.third_util.ml.np_util` - numpy 工具（可选）

## 测试文件
无对应的测试文件

## 修改注意事项
1. 浮点数比较使用固定容差 0.000001，可根据需要调整
2. JSON 转换异常时会抛出异常，确保输入数据格式正确
3. 键路径连接符可通过 `key_join_char` 自定义
4. numpy 数组比较支持自动张量转换
5. 递归深度受 Python 递归限制，大数据结构可能需要优化