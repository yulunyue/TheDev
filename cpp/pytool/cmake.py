from common.tool.export import (
    TableConfig,
    StrModel,
    ListModel,
    TableBase,
    OsUtil,
    NumberModel,
)
from common.util.export import File, logger
from .constant import C


class NodeConfig(TableConfig):
    src = StrModel()
    file_last_update_t = NumberModel()
    depends = ListModel()

    def get_target(self, is_root):
        return self.src.get_value() + (C.BIN_SUFFIX if is_root else C.LIB_SUFFIX)


class CMake:
    def __init__(self, src, resource="cpp_build"):
        self.source = TableBase[NodeConfig]().set_resource(resource)
        self.root = self.source.get(src)
        self.root.src.set_value(src)

    def make(self):
        self.make_node(self.root, is_root=True)

    def make_node(self, c: NodeConfig, is_root=False):
        for d in c.depends.get_value():
            self.make_node(d)
        m_time = int(File(c.src.get_value()).get_m_time())
        if m_time == c.file_last_update_t.get_value():
            return
        OsUtil(C.GCC).run(
            c.src.get_value(),
            C.I("./"),
            C.DEBUG_FLAG,
            C.O_FLAG,
            c.get_target(is_root),
        )
        c.file_last_update_t.set_value(m_time)
        return

    def execute(self):
        self.make()
        result = OsUtil(self.root.get_target(True)).run()
        logger.info(result)
        self.source.save()
