# FormBase 类分析

## 概述
`FormBase` 是一个继承自 `ApiBase` 的基类，提供了表单和表格视图的通用功能，用于处理前端表单交互和数据展示。

## 类结构

```python
class FormBase(ApiBase):
    model: ConfigBase = ConfigBase
```

### 类属性
- `model`: 指向 `ConfigBase` 类，用于数据模型操作

## 方法

### `get(key, **kw)`
- **功能**: 根据 key 获取模型数据
- **参数**: 
  - `key`: 键值
  - `**kw`: 其他关键字参数
- **返回**: 模型数据

### `to_form_row_view()`
- **功能**: 生成行式表单视图
- **返回**: `Form` 对象，设置为行布局，包含模型的所有字体列
- **实现**: 调用 `model.get_font_columns()` 获取列配置

### `to_form_column_view()`
- **功能**: 生成列式表单视图
- **返回**: `Form` 对象，设置为列布局，包含模型的所有字体列
- **实现**: 调用 `model.get_font_columns()` 获取列配置

### `web_submit(type, value: dict, **kw)`
- **功能**: 处理 Web 表单提交
- **参数**:
  - `type`: 提交类型
  - `value`: 提交的数据字典
  - `**kw`: 其他关键字参数
- **返回**: 包含保存数据的 `Node` 对象
- **实现流程**:
  1. 调用 `model.insert(**value)` 创建新记录
  2. 调用 `save()` 保存到存储
  3. 返回包含保存值的数据节点

### `web_search(key, name, **kw)`
- **功能**: 处理搜索请求，返回所有记录的列表
- **参数**:
  - `key`: 搜索键
  - `name`: 搜索名称
  - **kw**: 其他关键字参数
- **返回**: `Node` 对象，包含所有记录的子节点列表
- **实现**:
  - 遍历 `model.all()` 获取所有记录
  - 每条记录转换为包含 `title`（ID）和 `value`（记录对象）的字典

### `to_table_view()`
- **功能**: 生成表格视图
- **返回**: `FrontTable` 对象，包含表头和所有记录数据
- **实现流程**:
  1. 获取模型类
  2. 调用 `model.get_params()` 获取表头配置
  3. 调用 `model.all()` 获取所有记录作为表格内容

## 依赖关系

### 导入模块
- `common.tool.export`: `FrontTable`, `Form`, `ConfigBase`
- `common.util.export`: `Node`, `C`, `ApiBase`

### 基类
- `ApiBase`: 提供 API 基础功能

### 协作类
- `ConfigBase`: 数据模型基类
- `Form`: 表单生成类
- `FrontTable`: 前端表格类
- `Node`: 数据节点类

## 使用场景

该类主要用于：
1. 表单数据的提交和处理
2. 搜索和数据展示
3. 表格视图生成
4. 行式/列式表单视图生成

## 设计模式

- **模板方法模式**: 通过 `model` 属性提供数据操作模板
- **工厂模式**: 生成不同类型的视图（表单、表格）
- **适配器模式**: 将 `ConfigBase` 数据适配到前端展示格式

## 代码特点
1. 简洁轻量，仅36行代码
2. 高度抽象，通过 `model` 属性实现数据操作解耦
3. 提供完整的前端视图生成功能
4. 支持增删改查的基础操作