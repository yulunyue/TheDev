import time


def time_format(timestamp=None, fmt="%Y-%m-%d %H:%M:%S"):
    if timestamp is None:
        timestamp = time.time()
    time_struct = time.localtime(timestamp)
    format_date = time.strftime(fmt, time_struct)
    return format_date


DATAE_CHANGE_MAP = dict()


def time_change(fmt="%Y-%m-%d %H:%M:%S"):
    t = time_format(fmt=fmt)
    ret = DATAE_CHANGE_MAP.get(fmt) != t
    DATAE_CHANGE_MAP[fmt] = t
    return ret


def time_strptime(s: str, fmt="%Y-%m-%d %H:%M:%S"):
    timeArray = time.strptime(s, fmt)
    return time.mktime(timeArray)
