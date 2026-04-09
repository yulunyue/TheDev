from .chess_state import CState664
from common.util.export import Dict, Type


class CState333(CState664):
    w = 3
    h = 3
    in_row = 3
    STATE_STORE = dict()


CHESS_MAP_CLS_FUNC: Dict[str, Type[CState664]] = {CState664.__name__: CState664}
for cls in CState664.__subclasses__():
    CHESS_MAP_CLS_FUNC[cls.__name__] = cls
