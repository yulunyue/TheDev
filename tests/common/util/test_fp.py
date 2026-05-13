import unittest
import sys
import os
import tempfile
import shutil
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.util.fp import File


class TestFile(unittest.TestCase):
    """测试 File 类"""

    def setUp(self):
        """设置测试环境"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.txt")

        # 确保测试目录存在
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """清理测试环境"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_file_creation(self):
        """测试 File 对象创建"""
        file_obj = File(self.test_file)

        self.assertEqual(file_obj.path, self.test_file.replace("\\", "/"))
        self.assertEqual(file_obj.name, "test_file")
        self.assertEqual(file_obj.file_name, "test_file.txt")
        self.assertEqual(file_obj.type, "txt")
        self.assertFalse(file_obj.exists())

    def test_file_creation_without_extension(self):
        """测试没有扩展名的文件创建"""
        file_path = os.path.join(self.test_dir, "no_extension")
        file_obj = File(file_path)

        self.assertEqual(file_obj.name, "no_extension")
        self.assertEqual(file_obj.file_name, "no_extension")
        self.assertEqual(file_obj.type, "")

    def test_file_creation_with_multiple_extensions(self):
        """测试多扩展名的文件创建"""
        file_path = os.path.join(self.test_dir, "archive.tar.gz")
        file_obj = File(file_path)

        self.assertEqual(file_obj.name, "archive.tar")
        self.assertEqual(file_obj.file_name, "archive.tar.gz")
        self.assertEqual(file_obj.type, "gz")

    def test_file_creation_with_non_string_path(self):
        """测试非字符串路径"""
        with self.assertRaises(Exception):
            File(123)  # 应该抛出异常

    def test_make_dir_if_not_exist(self):
        """测试目录创建"""
        file_obj = File(self.test_file)

        # 创建文件和目录
        result = file_obj.make_dir_if_not_exist()
        self.assertEqual(result, file_obj)  # 返回 self 支持链式调用

        # 验证目录存在
        dir_path = os.path.dirname(self.test_file)
        self.assertTrue(os.path.exists(dir_path))

    def test_write_and_read_text_file(self):
        """测试文本文件的写入和读取"""
        file_obj = File(self.test_file)

        # 写入文本
        test_content = "Hello, World!"
        file_obj.write_file(test_content)

        # 验证文件存在
        self.assertTrue(file_obj.exists())

        # 读取文本
        content = file_obj.read_file()
        self.assertEqual(content, test_content)

    def test_write_and_read_json_file(self):
        """测试 JSON 文件的写入和读取"""
        file_obj = File(self.test_file + ".json")

        # 写入字典（自动转换为 JSON）
        test_data = {"key": "value", "number": 42, "list": [1, 2, 3]}
        file_obj.write_file(test_data)

        # 验证文件存在
        self.assertTrue(file_obj.exists())

        # 读取 JSON
        data = file_obj.read_file()
        self.assertEqual(data, test_data)

    def test_write_and_read_binary_file(self):
        """测试二进制文件的写入和读取"""
        file_obj = File(self.test_file)

        # 写入二进制数据
        test_data = b"Binary data: \x00\x01\x02\x03"
        file_obj.write_file(test_data)

        # 验证文件存在
        self.assertTrue(file_obj.exists())

        # 读取二进制数据
        data = file_obj.read_data()
        self.assertEqual(data, test_data)

    def test_write_if_not_exists(self):
        """测试条件写入"""
        file_obj = File(self.test_file)

        # 第一次写入
        result = file_obj.write_if_not_exists("first content")
        self.assertEqual(result, file_obj)
        self.assertEqual(file_obj.read_file(), "first content")

        # 第二次写入（应该不会覆盖）
        file_obj.write_if_not_exists("second content")
        self.assertEqual(file_obj.read_file(), "first content")

    def test_is_json_file(self):
        """测试 JSON 文件检测"""
        json_file = File(os.path.join(self.test_dir, "test.json"))
        txt_file = File(os.path.join(self.test_dir, "test.txt"))

        self.assertTrue(json_file.is_json_file())
        self.assertFalse(txt_file.is_json_file())

    def test_read_line(self):
        """测试按行读取"""
        file_obj = File(self.test_file)
        content = "Line 1\nLine 2\nLine 3"
        file_obj.write_file(content)

        lines = file_obj.read_line()
        expected = ["Line 1", "Line 2", "Line 3"]
        self.assertEqual(lines, expected)

    def test_copy_to(self):
        """测试文件复制"""
        source_file = File(self.test_file)
        dest_file = File(os.path.join(self.test_dir, "copy.txt"))

        # 写入源文件
        source_file.write_file("original content")

        # 复制文件
        result = source_file.copy_to(dest_file)
        self.assertEqual(result, dest_file)

        # 验证复制成功
        self.assertTrue(dest_file.exists())
        self.assertEqual(dest_file.read_file(), "original content")

    def test_copy_to_existing_file(self):
        """测试复制到已存在的文件"""
        source_file = File(self.test_file)
        dest_file = File(os.path.join(self.test_dir, "existing.txt"))

        # 写入源文件和目标文件
        source_file.write_file("original content")
        dest_file.write_file("existing content")

        # 复制文件（不覆盖）
        result = source_file.copy_to(dest_file, over_write=False)
        self.assertEqual(result, dest_file)

        # 验证目标文件内容未改变
        self.assertEqual(dest_file.read_file(), "existing content")

    def test_copy_to_overwrite(self):
        """测试覆盖复制"""
        source_file = File(self.test_file)
        dest_file = File(os.path.join(self.test_dir, "dest.txt"))

        # 写入源文件和目标文件
        source_file.write_file("new content")
        dest_file.write_file("old content")

        # 复制文件（覆盖）
        source_file.copy_to(dest_file, over_write=True)

        # 验证覆盖成功
        self.assertEqual(dest_file.read_file(), "new content")

    def test_move_to(self):
        """测试文件移动"""
        source_file = File(self.test_file)
        dest_file = File(os.path.join(self.test_dir, "moved.txt"))

        # 写入源文件
        source_file.write_file("moved content")

        # 移动文件
        result = source_file.move_to(dest_file)
        self.assertEqual(result, dest_file)

        # 验证移动成功
        self.assertFalse(source_file.exists())
        self.assertTrue(dest_file.exists())
        self.assertEqual(dest_file.read_file(), "moved content")

    def test_parent(self):
        """测试获取父目录"""
        file_obj = File(self.test_file)
        parent_obj = file_obj.parent()

        expected_parent = os.path.dirname(self.test_file).replace("\\", "/")
        self.assertEqual(parent_obj.path, expected_parent)
        self.assertTrue(parent_obj.is_dir())

    def test_child(self):
        """测试获取子文件"""
        file_obj = File(self.test_dir)
        child_obj = file_obj.child("subdir", "child_file.txt")

        expected_path = os.path.join(self.test_dir, "subdir", "child_file.txt").replace(
            "\\", "/"
        )
        self.assertEqual(child_obj.path, expected_path)

    def test_get_abs_path(self):
        """测试获取绝对路径"""
        file_obj = File(self.test_file)
        abs_path = file_obj.get_abs_path()

        self.assertTrue(abs_path.endswith(self.test_file.replace("\\", "/")))

    def test_get_size(self):
        """测试获取文件大小"""
        file_obj = File(self.test_file)
        content = "Hello, World!"
        file_obj.write_file(content)

        size = file_obj.get_size()
        self.assertGreater(size, 0)

    def test_get_m_time(self):
        """测试获取修改时间"""
        file_obj = File(self.test_file)
        file_obj.write_file("test content")

        m_time = file_obj.get_m_time()
        self.assertIsInstance(m_time, float)
        self.assertGreater(m_time, 0)

    def test_get_m_time_str(self):
        """测试获取格式化的修改时间"""
        file_obj = File(self.test_file)
        file_obj.write_file("test content")

        m_time_str = file_obj.get_m_time_str()
        self.assertIsInstance(m_time_str, str)
        self.assertGreater(len(m_time_str), 0)

    def test_remove(self):
        """测试文件删除"""
        file_obj = File(self.test_file)
        file_obj.write_file("to be deleted")

        # 验证文件存在
        self.assertTrue(file_obj.exists())

        # 删除文件
        result = file_obj.remove()
        self.assertEqual(result, file_obj)

        # 验证文件已删除
        self.assertFalse(file_obj.exists())

    def test_remove_nonexistent_file(self):
        """测试删除不存在的文件"""
        file_obj = File(self.test_file)

        # 删除不存在的文件
        result = file_obj.remove()
        self.assertEqual(result, file_obj)

    def test_replace_content(self):
        """测试文件内容替换"""
        file_obj = File(self.test_file)
        file_obj.write_file("original content")

        # 替换内容
        replacements = {"original": "new", "content": "data"}
        file_obj.replace(replacements)

        # 验证替换成功
        self.assertEqual(file_obj.read_file(), "new data")

    def test_list_dir(self):
        """测试列出目录内容"""
        # 创建测试文件
        file1 = File(os.path.join(self.test_dir, "file1.txt"))
        file2 = File(os.path.join(self.test_dir, "file2.txt"))
        subdir = File(os.path.join(self.test_dir, "subdir"))

        file1.write_file("content1")
        file2.write_file("content2")
        subdir.make_dir_if_not_exist()

        dir_obj = File(self.test_dir)
        files = dir_obj.list_dir()

        # 验证找到文件
        self.assertGreaterEqual(len(files), 2)
        file_names = [f.name for f in files]
        self.assertIn("file1", file_names)
        self.assertIn("file2", file_names)

    def test_is_dir_and_is_file(self):
        """测试目录和文件检测"""
        file_obj = File(self.test_file)
        dir_obj = File(self.test_dir)

        self.assertFalse(file_obj.is_dir())
        self.assertFalse(file_obj.is_file())

        file_obj.write_file("test")
        self.assertTrue(file_obj.is_file())
        self.assertFalse(file_obj.is_dir())

        self.assertTrue(dir_obj.is_dir())
        self.assertFalse(dir_obj.is_file())

    def test_get_writer(self):
        """测试获取文件写入器"""
        file_obj = File(self.test_file)
        file_obj.make_dir_if_not_exist()

        writer = file_obj.get_writer()
        self.assertIsNotNone(writer)

        # 写入测试
        writer.write(b"test line\n")
        writer.flush()

        # 验证写入成功
        self.assertEqual(file_obj.read_file(), "test line\n")
        writer.close()


class TestFileClassMethods(unittest.TestCase):
    """测试 File 类的类方法"""

    def setUp(self):
        """设置测试环境"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.txt")

    def tearDown(self):
        """清理测试环境"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_new_method(self):
        """测试 new 方法"""
        file1 = File.new(self.test_file)
        file2 = File.new(self.test_file)

        # 应该返回相同的实例（缓存）
        self.assertIs(file1, file2)

    def test_file_cache(self):
        """测试文件缓存"""
        file1 = File(self.test_file)
        file2 = File(self.test_file)

        # 不同实例
        self.assertIsNot(file1, file2)

        # 使用 new 方法应该是同一个实例
        file3 = File.new(self.test_file)
        file4 = File.new(self.test_file)
        self.assertIs(file3, file4)

    def test_file_wb(self):
        a = File("data/tmp/a.txt")
        f = a.get_bin_writer("wb+")
        f.write(b"123")
        f.flush()
        self.assertEqual(a.read_data(), b"123")
        f.write(b"4")
        f.flush()
        self.assertEqual(a.read_data(), b"1234")


if __name__ == "__main__":
    unittest.main()
