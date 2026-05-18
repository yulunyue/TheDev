from common.util.export import File


class FileChange:
    def __init__(self, filename, **kw):
        self.filename: str = filename
        if not isinstance(filename, str):
            raise Exception(filename)

    def set_local(self, root: File):
        self.root: File = root
        self.local: File = root.child(self.filename)
        return self

    def to_json(self):
        return {"filename": self.filename}