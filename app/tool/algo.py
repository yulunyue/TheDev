from common.util.export import (
    ApiBase,
    File,
    Node,
    Module,
    MockCf,
    logger,
    C,
    execute_by_thread,
)
from common.tool.export import TableBase

ROOT = File("app/yly/algo")


def get_module_file(path):
    try:
        ret = Module().load_module_object(path + "::Solution")()
        return ret
    except Exception as e:
        logger.exception(e, stack_info=True)


class Algo(ApiBase):
    def search(self, **kw):
        nodes = []
        for f in ROOT.list_tree_file():
            if not f.file_name.endswith(".py"):
                continue
            ins: MockCf = get_module_file(f.path)
            if ins is None:
                continue
            for case, value in ins.get_cases().items():
                nodes.append(
                    Node(
                        key=f"{f.name}_{case}",
                        value=dict(path=f.path, case=value, code=f.read_file()),
                    )
                )
        return Node(childs=nodes)

    def run(self, code, **kw):
        v: dict = code[C.K_VALUE]
        path, case, code = v["path"], v["case"], v["code"]
        tmp_path = "data/algo/tmp.py"
        File(tmp_path).write_file(code)
        m: MockCf = Module().load_module_object(tmp_path + "::Solution")()
        return Node(data=execute_by_thread(m, case))


if __name__ == "__main__":
    logger.info(Algo().search())
