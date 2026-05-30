from common.third_util.dataa.excel_util import PandasUtil
from common.util.export import File
from common.tool.export import ToolBase


class ExcelTool(ToolBase):
    def convert_yo_json(self, path: str):
        f = File(path)
        if f.is_file():
            PandasUtil().load(f.path).dump_json()
            return
        for c in f.list_dir():
            if c.is_file() and PandasUtil.is_excel_file(c.type):
                PandasUtil().load(c.path).dump_json()


if __name__ == "__main__":
    ExcelTool().run()
