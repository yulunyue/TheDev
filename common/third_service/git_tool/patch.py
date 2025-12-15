from common.util.export import File, List
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
            if s.startswith("+++ b/"):
                f = FileChange(s[6:]).set_local(self.pr.local)
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

    def make_patch(self, path: str, name):
        for p in path.split(" "):
            logger.info(self.local_repo.child(p))
        input(f"WAIT {name}")
        self.git_cmd.run("add", ".")
        self.git_cmd.run("config", "--global", "user.name", "xx", env=dict(HOME="./"))
        self.git_cmd.run(
            "config", "--global", "user.email", "xx@xx.com", env=dict(HOME="./")
        )
        self.git_cmd.run(
            "commit",
            "-m",
            name,
            env=dict(GIT_AUTHOR_NAME="xx", GIT_AUTHOR_EMAIL="xx@xx.com", HOME="./"),
        )
        # self.git_cmd.run("switch", "-c", f"zzb_{name}_branch")
        self.git_cmd.run("format-patch", "-1")
        ret = self.local_repo.child(f"0001-{name}.patch").read_file()
        return ret
