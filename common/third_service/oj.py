from common.util.export import logger, MockCf, get_file_path_by_cls, Module, get_dev_log
from common.tool.export import PyFile


def oj_run(ins: MockCf, case_name=None):
    cases: dict = ins.get_cases()
    if case_name:
        cases = [[case_name, cases[case_name]]]
    else:
        cases = cases.items()
    for case_name, c in cases:
        exp = c.pop("result")
        ins.logger = get_dev_log(case_name)
        res = ins.execute(**c)
        if res != exp:
            logger.info(f"FAILED {case_name} {exp}!={res}")
        else:
            logger.info(f"PASS {case_name} {exp}=={res}")
    src_file = ins.src_file
    if src_file is None:
        src_file = get_file_path_by_cls(ins.__class__)
    PyFile(src_file).compile_to_one_file()
