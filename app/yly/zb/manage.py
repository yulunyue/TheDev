from common.util.export import ToolBase
from .util import WT


class ZbMangae(ToolBase):
    def query(self):
        WT.start()


if __name__ == "__main__":
    ZbMangae().run()
