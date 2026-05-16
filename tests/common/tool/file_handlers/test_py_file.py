from common.util.export import TestBase, logger, Module
from common.tool.file_handlers.py_file import PyFile


class TestPyFile(TestBase):
    def test_base(self):
        pf = PyFile(__file__)
        pf.compile_to_one_file()
        self.expect(
            list(pf.depends.keys()),
            ["common/mock.py", "common/tool/file_handlers/py_file.py"],
        )
