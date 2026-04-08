# XMLJSON 模块文档

## 文件概述
`xmljson.py` 提供了 XML 和 JSON 格式之间的相互转换功能，支持从文件或字典数据创建 XML 结构，并能将 XML 转换为 JSON 格式。

## 主要功能

### 工具函数
- `int_util(v)`: 尝试将值转换为整数
  - 成功则返回整数，失败则返回原值

### XmlUtil 类
**用途**: XML 和 JSON 格式转换器

**属性**:
- `namespace`: XML 命名空间
- `attr_key`: 属性键名，默认为 "attr"
- `child_key`: 子元素键名，默认为 "children"
- `node_key`: 节点键名，默认为 "node"
- `_tree`: XML 树对象
- `_root`: XML 根元素

**构造函数**:
- `__init__(data: str, namespace=None)`: 初始化 XML 工具
  - `data` 可以是:
    - dict: 直接转换为 XML
    - 字符串: 如果以 ".json" 结尾，从 JSON 文件加载
    - 字符串: 如果以 ".xml" 结尾，解析 XML 文件

**主要方法**:

**转换方法**:
- `toJson()`: 将 XML 转换为 JSON 格式
  - 返回结构: {node: "tag", attr: {...}, children: [...]}
- `dictToXml(oj)`: 将字典转换为 XML
  - 递归处理嵌套字典结构
  - 支持属性和子元素

**文件操作**:
- `save(path: str)`: 保存到文件
  - 根据文件扩展名选择格式 (JSON/XML)
- `toString()`: 将 XML 转换为字符串

**访问和修改**:
- `get(keys)`: 获取指定路径的元素
- `__setitem__(key, value)`: 设置元素属性值
- `__getitem__(key)`: 获取元素属性值

### 便捷函数
- `M(_node_tmp_name, *args, **kwargs)`: 创建 XML 节点字典
  - 自动构建符合 XmlUtil 格式的字典结构

## 使用示例

```python
from common.util.xmljson import XmlUtil, M

# 从 JSON 文件创建 XML
xml_util = XmlUtil("data.json")
xml_str = xml_util.toString()
xml_util.save("output.xml")

# 从字典创建 XML
data = {
    "node": "root",
    "attr": {"version": "1.0"},
    "children": [
        {"node": "child1", "attr": {"id": "1"}},
        {"node": "child2", "attr": {"id": "2"}}
    ]
}
xml_util = XmlUtil(data)
xml_util.save("from_dict.xml")

# XML 转 JSON
json_data = xml_util.toJson()
print(json_data)

# 使用便捷函数创建节点
node_dict = M("root", 
              M("child1", "text1"),
              M("child2", "text2"),
              attr={"version": "1.0"})
xml_util = XmlUtil(node_dict)
xml_util.save("complex.xml")

# 访问和修改元素
value = xml_util["root/child1"]  # 获取值
xml_util["root/child1"] = "new_value"  # 设置值
```

## 数据结构映射

### XML 到 JSON 的映射
```xml
<root version="1.0">
    <child id="1">text</child>
</root>
```

转换为 JSON:
```json
{
    "node": "root",
    "attr": {"version": "1.0"},
    "children": [
        {
            "node": "child",
            "attr": {"id": "1"},
            "children": ["text"]
        }
    ]
}
```

### 便捷函数 M()
```python
# M 函数可以创建复杂的 XML 结构
root = M("root",
         M("person", 
           M("name", "John"),
           M("age", "30"),
           M("address", 
             M("street", "123 Main St"),
             M("city", "New York")
           )
         ),
         attr={"type": "personal"})
```

## 依赖关系
- `typing.Dict` - 类型提示
- `xml.etree.ElementTree as ET` - XML 处理
- `common` - 项目模块
- `json` - JSON 处理
- `re` - 正则表达式

## 测试文件
无对应的测试文件

## 修改注意事项
1. XML 元素名和属性名需要符合 XML 规范
2. 字典键名会被直接用作 XML 标签名，需要注意命名规则
3. 文件路径处理需要确保文件存在且格式正确
4. 命名空间支持有限，复杂命名空间可能需要额外处理
5. XML 转换过程会丢失部分 XML 特性，如注释、CDATA 等
6. 大型 XML 文件处理时需要注意内存使用