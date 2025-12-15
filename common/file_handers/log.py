from common.util.export import File, List


class LnResults:
    pass


class LogFileAna:
    def __init__(self, f):
        self.f: File = f if isinstance(f, File) else File(f)
        self.results = None

    def get_results(self):
        for ln in self.f.read_line():
            pass
