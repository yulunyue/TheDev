import os
from typing import List
import json
from common.util.log import logger


def os_system(s: str):
    ret = os.system(s)
    if ret != 0:
        raise Exception(s)
