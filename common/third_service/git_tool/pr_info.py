from common.util.export import List, File
from .file_change_model import FileChange
from .patch import Patch
from .git_api import GitHubApi


class PrInfo:
    title = None

    def set_owner(self, owner):
        self.owner = owner
        return self

    def load(self, title="", **kw):
        self.title = title
        return self

    def get_title(self):
        self.get_config()
        return self.title

    def get_isure(self):
        try:
            return int(self.get_title().split("#").pop())
        except Exception as e:
            return None

    def set_repo(self, repo):
        self.repo = repo
        return self

    def set_local(self, local):
        self.local: File = local
        return self

    def set_number(self, number):
        self.number = number
        return self

    def __init__(self, files: List[dict] = None, **kwargs):
        self.files = [FileChange(**d) for d in files or []]

    def get_patch(self, f: File):

        return Patch().set_file(f).set_pr(self)

    config = None

    def get_config(self):
        if self.config is None:
            self.config = (
                GitHubApi().load(self.owner, self.repo).get_pr_info(self.number)
            )
            self.load(**self.config["files"])
        return self.config

    def to_json(self):
        return dict(title=self.title)
