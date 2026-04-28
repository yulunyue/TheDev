from .chess_state import CState664
from common.util.export import Dict, Type


class CState333(CState664):
    w = 3
    h = 3
    in_row = 3
    STATE_STORE = dict()
    name = "C333"


CHESS_MAP_CLS_FUNC: Dict[str, Type[CState664]] = {CState664.name: CState664}
for cls in CState664.__subclasses__():
    CHESS_MAP_CLS_FUNC[cls.name] = cls
