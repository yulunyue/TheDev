from common.util.export import logger, MockCf, get_file_path_by_cls, Module


def oj_run(ins: MockCf, case_name=None):
    cases: dict = ins.get_cases()
    if case_name:
        cases = [case_name, cases[case_name]]
    else:
        cases = cases.items()
    for case_name, c in cases:
        exp = c.pop("result")
        res = ins.execute(**c)
        if exp != exp:
            logger.map(inp=c, res=res, exp=exp)
        else:
            logger.info(f"{case_name} PASS")
    Module().compile_one(get_file_path_by_cls(ins.__class__))
