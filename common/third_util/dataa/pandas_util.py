import pandas as pd

from common.util.export import List, File, TempFile


class PandasUtil:
    @classmethod
    def is_excel_file(cls, name):
        return name in {"xlsx"}

    def dump_json(self):
        File(self.path + ".json").write_file(self.to_json())

    def load(self, path: str):
        self.path = path
        self.instance = pd.read_excel(path)
        return self

    def get_info(self):
        f = TempFile(TempFile.STR_MODE)
        self.instance.info(buf=f)
        return f.data

    def group_by(self, *keys):
        ret = dict()
        for index, row in self.instance.iterrows():
            k = "|".join(row[key] for key in keys)
            ret[k] = ret.get(k, 0) + 1
        return ret

    def head(self, n="1"):
        return self.instance.head(int(n))

    def hander(self, method, *args):
        return getattr(self, method)(*args)

    def to_json(self):
        return self.instance.to_json(force_ascii=False, orient="columns")

    def load_sheet(self, path: str, sheet_name: str):
        """读取指定 sheet"""
        self.path = path
        self.instance = pd.read_excel(path, sheet_name=sheet_name)
        return self

    def load_all_sheets(self, path: str):
        """读取所有 sheet，返回 dict"""
        self.path = path
        self.sheets = pd.read_excel(path, sheet_name=None)
        return self

    def get_sheet(self, sheet_name: str):
        """获取指定 sheet 的 DataFrame"""
        if hasattr(self, 'sheets'):
            return self.sheets.get(sheet_name)
        return None

    def set_value(self, row_idx: int, col_name: str, value):
        """设置指定行列的值"""
        self.instance.loc[row_idx, col_name] = value
        return self

    def save_excel(self, output_path: str, sheets: dict = None, format: str = "xlsx"):
        """保存 Excel 文件"""
        if sheets is None:
            sheets = {"Sheet1": self.instance}

        if format == "xls":
            import win32com.client.dynamic
            import os
            
            excel = win32com.client.dynamic.Dispatch("Excel.Application")
            
            wb = excel.Workbooks.Add()
            
            sheet_names = list(sheets.keys())
            for i, df in enumerate(sheets.values()):
                if i == 0:
                    ws = wb.Worksheets(1)
                    ws.Name = sheet_names[i]
                else:
                    ws = wb.Worksheets.Add()
                    ws.Name = sheet_names[i]
                
                for col_idx, col_name in enumerate(df.columns):
                    ws.Cells(1, col_idx + 1).Value = str(col_name) if not pd.isna(col_name) else ""
                
                for row_idx, row in df.iterrows():
                    for col_idx, value in enumerate(row):
                        cell = ws.Cells(row_idx + 2, col_idx + 1)
                        if pd.isna(value):
                            cell.Value = ""
                        elif isinstance(value, pd.Timestamp):
                            cell.Value = str(value)
                        elif isinstance(value, (int, float)):
                            cell.Value = value
                        else:
                            cell.Value = str(value)
            
            wb.SaveAs(os.path.abspath(output_path), FileFormat=56)  # 56 = xls format
            wb.Close(SaveChanges=False)
            excel.Quit()
            
            # 确保 Excel 进程完全退出
            import time
            time.sleep(0.5)
        else:
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for sheet_name, df in sheets.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return output_path
