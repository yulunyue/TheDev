from common.util.export import ToolBase
from .util import WT


class ZbMangae(ToolBase):
    def query(self):
        WT.run()


if __name__ == "__main__":
    ZbMangae().run()
