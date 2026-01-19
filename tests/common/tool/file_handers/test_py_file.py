from common.util.export import TestBase, logger, Module
from common.tool.file_handers.py_file import PyFile


class TestPyFile(TestBase):
    def test_base(self):
        root = PyFile(__file__).save_to_one_file()
        self.expect(
            list(root.depends.keys()),
            ["common/mock.py", "common/tool/file_handers/py_file.py"],
        )
