from common.util.export import ToolBase, Module, logger


class CgTool(ToolBase):
    def pk(self, path):
        Module().compile_one(path)

    def cg(self):
        CodingGame(Cgl9.name).pk(Module.RUN_TMP_PATH, Cgl9.game_id, Cgl9.agentsIds)


if __name__ == "__main__":
    pass
