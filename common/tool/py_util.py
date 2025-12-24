from .os_util import OsUtil
from .global_config import GC
from common.util.export import logger
import sys


class PyUtil(OsUtil):
    def __init__(self):
        super().__init__(sys.executable)

    def pip_download(
        self,
        pkg,
        out_put="data/site-packages",
        platform="manylinux2014_x86_64",
        ob=False,
        py_version=None,
    ):
        """
        Docstring for pip_download

        :param self: Description
        :param pkg: Description
        :param platform: Description manylinux2014_x86_64 or manylinux2014_x86_64
        """

        kw = {
            "-d": out_put,
            "-i": GC.pip_global_index_url.get_value(),
            "--trusted-host": GC.pip_trusted_host.get_value(),
        }
        if platform:
            kw["--platform"] = platform
        if py_version:
            kw["--python-version"] = py_version
        args = []
        if ob:
            args.append("--only-binary=:all:")
        # else:
        #     args.append("--no-binary=:none:")
        self.run("-m", "pip", "download", "--no-deps", pkg, *args, **kw)
        logger.info(f"python3 -m pip install --no-index --find-links=./ {pkg} --user")
        return out_put
