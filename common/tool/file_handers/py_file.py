from common.util.export import File, Dict, logger
from common.tool.export import StrUtil, ReUtil


class PyFile:
    RUN_TMP_PATH = "data/algo/run.py"
    VT: Dict[str, "PyFile"] = dict()
    TMP_VT = set()

    def __init__(self, path: str):
        self.fp = File(path)
        self.lines = []
        self.depends: Dict[str, PyFile] = dict()

    def model_mock(self, model_name: str) -> tuple[str, bool]:
        need_read = False
        if ReUtil("common.*export").findall(model_name):
            model_name = "common.mock"
            need_read = True
        elif model_name.startswith("common"):
            need_read = True
        # logger.info(model_name)
        return model_name, need_read

    def read_lines(self):
        if not self.lines:
            self.load()
        lines = []
        for k, d in self.depends.items():
            if k not in self.TMP_VT:
                self.TMP_VT.add(k)
                lines.extend(d.read_lines())
        return lines + self.lines

    def load(self):
        self.lines = []
        for ln2 in self.fp.read_line():
            if not ln2:
                continue
            ln = ln2.strip()
            if ln2.startswith("from"):
                ln = ln2.strip().split(" ")[1]
                if ln.startswith("."):
                    ln = self.fp.get_relative_path(ln)
                ln, need_read = self.model_mock(ln)
                if need_read:
                    path = ln.replace(".", "/") + ".py"
                    if path not in PyFile.VT:
                        PyFile.VT[path] = PyFile(path)
                    self.depends[path] = PyFile.VT[path]
                else:
                    self.lines.append(ln2)
            else:
                self.lines.append(ln2)
        return self

    def compile_to_one_file(self):
        temp_py_file = File(self.RUN_TMP_PATH)
        PyFile.TMP_VT = {self.fp.path}
        logger.info(self.fp)
        logger.info(temp_py_file.write_file("\n".join(self.read_lines())))
        return self
