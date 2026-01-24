from common.util.export import File, List, logger
from .file_change_model import FileChange


class Patch:
    def __init__(self):
        self.file_changes: List[FileChange] = None

    def set_file(self, f):
        self.f: File = f
        return self

    def set_pr(self, pr):
        from .pr_info import PrInfo

        self.pr: PrInfo = pr
        return self

    def get_change_files(self):
        if self.file_changes is not None:
            return self.file_changes
        self.file_changes = []
        for s in self.f.read_line():
            if s.startswith("diff --git "):
                f = FileChange(s.split(" ")[-1][2:]).set_local(self.pr.local)
                self.file_changes.append(f)
        return self.file_changes

    def patch_repair(self, path=""):
        self.re_init()
        self.rest_repo()
        self.apply_patch(self.test_patch)
        self.apply_patch(self.code_patch)
        data = self.make_patch(path, "test")
        self.test_patch.write_file(data)
        self.cfg.test_patch.set_value(data)
        data = self.make_patch(path, "code")
        self.code_patch.write_file(data)
        self.cfg.patch.set_value(data)
