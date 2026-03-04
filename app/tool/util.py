from common.third_util.crypto.crypto_util import CryptoGraphy
from common.util.export import Node, b64_code, File
from common.tool.export import DomFile, FrontTable


class Util:
    API_ROUTE = "/app/util"

    def cert_dump(self, data: str, **kw):
        return Node(value=CryptoGraphy().load_from_data(data))

    def b64_code(self, code: str, **kw):
        return Node(value=b64_code(code))
