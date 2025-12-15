from common.util.export import List, File
from .file_change_model import FileChange
from .patch import Patch


class PrInfo:
    def set_owner(self, owner):
        self.owner = owner
        return self

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
