from common.util.export import logger, MockCf, get_file_path_by_cls, Module, get_dev_log


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
            logger.info(f"{case_name} {exp}!={res} FAILED")
        else:
            logger.info(f"{case_name} {exp}=={res} PASS")
    Module().compile_one(get_file_path_by_cls(ins.__class__))
