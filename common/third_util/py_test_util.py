import pytest
from common.util.export import logger
import urllib3
from coverage import Coverage

urllib3.disable_warnings()


class PyTestUtil:
    def __init__(self):
        self.flag_map = {
            # "--show-capture": "log",
            "--log-file": "data/log/pytest.log",
        }
        self.flags = ["--json-report --json-report-file=result.json"]

    def debug(self):
        """--full-trace"""
        self.flag_map["-vs"] = ""
        return self

    def set_root(self, path):
        self.flag_map["--rootdir"] = path
        return self

    def set_aim(self, *args):
        self.flags.extend(args)
        return self

    def main(self):
        flags = self.flags[:]
        for k, v in self.flag_map.items():
            if v:
                flags.append(f"{k}={v}")
            else:
                flags.append(k)
        logger.info(flags)
        pytest.main(flags)

    def coverage(self):

        cov = Coverage()
        cov.start()
        self.main()
        cov.stop()
        cov.html_report(directory="data/coverage")
