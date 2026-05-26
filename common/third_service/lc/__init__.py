from .client import LcClient
from .problem import LcProblemService
from .test import LcTestService
from .config import LANG, CODE_DIR, CACHE_DIR, LcCache
from .error import LcError
from .parser import LcContentParser


def get_lc_service() -> LcClient:
    return LcClient()


__all__ = [
    "LcClient",
    "LcProblemService",
    "LcTestService",
    "LcCache",
    "LcError",
    "LcContentParser",
    "get_lc_service",
    "LANG",
    "CODE_DIR",
    "CACHE_DIR",
]
