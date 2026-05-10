import pytest
from common.util.export import logger, File
import urllib3

urllib3.disable_warnings()


class PyTestUtil:
    def __init__(self):
        self.flag_map = {
            "--html": "data/coverage/pytest_report.html"
            # "--show-capture": "log",
            # "--log-file": "data/log/pytest.log",
        }
        self.flags = [
            "-l",
            "-vv",
            "-s",
        ]  # ["--json-report --json-report-file=result.json"]
        self.debug()

    def debug(self):
        """--full-trace"""
        self.flag_map["-vs"] = ""
        return self

    def set_root(self, path):
        self.flag_map["--rootdir"] = path
        return self

    def set_aim(self, *files):
        self.flags.extend([d.path if isinstance(d, File) else d for d in files])
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
        from coverage import Coverage

        cov = Coverage(source_dirs=["common", "app"])
        cov.start()
        self.main()
        cov.stop()
        cov.html_report(directory="data/coverage")
